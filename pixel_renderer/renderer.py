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
# Pillow's FreeType must be loaded before Pango: GI loads Pango with RTLD_GLOBAL, after which Pillow's
# bundled FreeType/HarfBuzz would bind to the system libraries and corrupt SignWriting rendering.
# See https://github.com/sign/pixel-renderer/issues/16
from PIL import ImageFont  # noqa: E402, F401, I001
from gi.repository import Pango, PangoCairo  # noqa: E402

_MIN_CANVAS_WIDTH = 1024


@cache
def _get_layout() -> Pango.Layout:
    """A reusable Pango layout, shared by all calls."""
    context = cairo.Context(cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1))
    try:
        return PangoCairo.create_layout(context)
    except KeyError as e:
        if "could not find foreign type Context" in str(e):
            raise RuntimeError("Pango/Cairo not properly installed. See https://github.com/sign/WeLT/issues/31") from e
        raise


_canvases = {}


def _get_canvas(height: int, width: int):
    """A reusable (surface, context, pixels) canvas per height, grown when a wider one is needed."""
    canvas = _canvases.get(height)
    if canvas is None or canvas[0].get_width() < width:
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, max(width, _MIN_CANVAS_WIDTH), height)
        context = cairo.Context(surface)
        context.set_source_rgb(0, 0, 0)  # Text is always black
        pixels = np.frombuffer(surface.get_data(), dtype=np.uint8).reshape(height, surface.get_stride() // 4, 4)
        canvas = _canvases[height] = (surface, context, pixels)
    return canvas


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
    return np.array(new_image, dtype=np.uint8)


@cache
def cached_font_description(font_name: str, font_size: int) -> Pango.FontDescription:
    return Pango.font_description_from_string(f"{font_name} {font_size}px")


def render_text(text: str, block_size: int = 16, font_size: int = 12) -> np.ndarray:
    """
    Renders text in black on white background using PangoCairo.

    Args:
        text (str): The text to render on a single line
        block_size (int): Height of each line in pixels, and width scale (default: 16)
        font_size (int): Font size (default: 12)

    Returns:
        np.ndarray: Rendered image with text
    """
    if is_swu(text):
        return render_signwriting(text, block_size=block_size)

    layout = _get_layout()
    layout.set_font_description(cached_font_description("sans", font_size))
    layout.set_text(visualize_control_tokens(text, include_whitespace=True), -1)
    text_width, text_height = layout.get_pixel_size()

    # Add padding and round up to nearest multiple of block_size
    width = dim_to_block_size(text_width + 10, block_size=block_size)

    surface, context, pixels = _get_canvas(block_size, width)
    pixels = pixels[:, :width]
    pixels.fill(255)  # White background, only the area we need
    surface.mark_dirty()

    # Left-aligned with a small padding, vertically centered
    context.move_to(5, (block_size - text_height) // 2)
    PangoCairo.show_layout(context, layout)
    surface.flush()

    return bgra_to_rgb(pixels)


def render_text_image(text: str, block_size: int = 16, font_size: int = 12) -> Image.Image:
    img_array = render_text(text, block_size=block_size, font_size=font_size)
    return Image.fromarray(img_array)
