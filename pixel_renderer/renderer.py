from functools import cache

import cairo
import gi
import numpy as np
from PIL import Image
from signwriting.formats.swu import is_swu
from signwriting.visualizer.visualize import signwriting_to_image
from utf8_tokenizer.control import visualize_control_tokens

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
gi.require_foreign("cairo")
from gi.repository import Pango, PangoCairo  # noqa: E402

# Reusable measurement context - avoids creating new surface/context/layout per call
# This provides ~10% speedup by reusing Pango layout object
_measurement_context = None

# Reusable rendering surface - avoids creating new surface per call
# Keyed by block_size (height), provides ~10% additional speedup
_render_surfaces = {}
_MAX_RENDER_WIDTH = 1024  # Max width for reusable surface


def _get_measurement_layout():
    """Get or create a reusable Pango layout for text measurement."""
    global _measurement_context
    if _measurement_context is None:
        temp_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
        temp_ctx = cairo.Context(temp_surface)
        try:
            layout = PangoCairo.create_layout(temp_ctx)
        except KeyError as e:
            if "could not find foreign type Context" in str(e):
                raise RuntimeError(
                    "Pango/Cairo not properly installed. See https://github.com/sign/WeLT/issues/31"
                ) from e
            raise
        _measurement_context = (temp_surface, temp_ctx, layout)
    return _measurement_context[2]


def _get_render_surface(block_size: int):
    """Get or create a reusable rendering surface for the given block size."""
    if block_size not in _render_surfaces:
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, _MAX_RENDER_WIDTH, block_size)
        context = cairo.Context(surface)
        _render_surfaces[block_size] = (surface, context)
    return _render_surfaces[block_size]


def dim_to_block_size(value: int, block_size: int) -> int:
    return ((value + block_size - 1) // block_size) * block_size


def bgra_to_rgb(bgra: np.ndarray) -> np.ndarray:
    """Convert BGRA/BGRX array to RGB.

    Cairo stores pixels as BGRX on little-endian systems. This function
    converts to RGB using pre-allocated array assignment, which is ~12%
    faster than fancy indexing (e.g., bgra[:, :, [2, 1, 0]]).

    Args:
        bgra: Array of shape (height, width, 4) with BGRA pixel data

    Returns:
        Array of shape (height, width, 3) with RGB pixel data
    """
    height, width = bgra.shape[:2]
    rgb = np.empty((height, width, 3), dtype=np.uint8)
    rgb[..., 0] = bgra[..., 2]  # R
    rgb[..., 1] = bgra[..., 1]  # G
    rgb[..., 2] = bgra[..., 0]  # B
    return rgb


def render_signwriting(text: str, block_size: int = 16) -> np.ndarray:
    image = signwriting_to_image(text, trust_box=False)
    width = dim_to_block_size(image.width + 10, block_size=block_size)
    height = dim_to_block_size(image.height + 10, block_size=block_size)
    new_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    padding = (width - image.width) // 2, (height - image.height) // 2
    new_image.paste(image, padding, image)
    # Explicitly convert PIL Image to numpy array with np.array() before ascontiguousarray()
    # This ensures correct shape interpretation regardless of PIL's internal buffer layout
    arr = np.array(new_image, dtype=np.uint8)
    return np.ascontiguousarray(arr)


@cache
def cached_font_description(font_name: str, font_size: int) -> Pango.FontDescription:
    return Pango.font_description_from_string(f"{font_name} {font_size}px")


def render_text(text: str, block_size: int = 16, font_size: int = 12) -> np.ndarray:
    """
    Renders text in black on white background using PangoCairo.

    Args:
        text (str): The text to render on a single line
        block_size (int): Height of each line in pixels, and width scale (default: 32)
        font_size (int): Font size (default: 12)

    Returns:
        np.ndarray: Rendered image with text
    """
    if is_swu(text):
        return render_signwriting(text, block_size=block_size)

    text = visualize_control_tokens(text, include_whitespace=True)

    # Get reusable layout for text measurement (avoids creating new surface/context/layout each call)
    layout = _get_measurement_layout()

    # Set font and measure text
    font_desc = cached_font_description("sans", font_size)
    layout.set_font_description(font_desc)
    layout.set_text(text, -1)
    text_width, text_height = layout.get_pixel_size()

    # Add padding and round up to nearest multiple of block_size
    width = dim_to_block_size(text_width + 10, block_size=block_size)
    line_height = block_size

    # Get reusable surface if width fits, otherwise create new one
    if width <= _MAX_RENDER_WIDTH:
        surface, context = _get_render_surface(block_size)
        surface_width = _MAX_RENDER_WIDTH
    else:
        # Text too wide for reusable surface, create dedicated one
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, line_height)
        context = cairo.Context(surface)
        surface_width = width

    # Fill white background (only the area we need)
    context.set_source_rgb(1.0, 1.0, 1.0)
    context.rectangle(0, 0, width, line_height)
    context.fill()

    # Set black text color
    context.set_source_rgb(0.0, 0.0, 0.0)

    # Position text (left-aligned horizontally, vertically within its line)
    x = 5  # Small left padding
    y = (line_height - text_height) // 2
    context.move_to(x, y)

    # Render text
    PangoCairo.show_layout(context, layout)

    # Extract image data as numpy array
    data = surface.get_data()
    bgra = np.frombuffer(data, dtype=np.uint8).reshape((line_height, surface_width, 4))
    # Slice to actual width if using reusable surface
    if surface_width > width:
        bgra = bgra[:, :width, :]
    return bgra_to_rgb(bgra)


def render_text_image(text: str, block_size: int = 16, font_size: int = 12) -> Image.Image:
    img_array = render_text(text, block_size=block_size, font_size=font_size)
    return Image.fromarray(img_array)
