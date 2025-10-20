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


def dim_to_block_size(value: int, block_size: int) -> int:
    return ((value + block_size - 1) // block_size) * block_size


def render_signwriting(text: str, block_size: int = 16) -> np.ndarray:
    image = signwriting_to_image(text, trust_box=False)
    width = dim_to_block_size(image.width + 10, block_size=block_size)
    height = dim_to_block_size(image.height + 10, block_size=block_size)
    new_image = Image.new("RGB", (width, height), color=(255, 255, 255))
    padding = (width - image.width) // 2, (height - image.height) // 2
    new_image.paste(image, padding, image)
    return np.array(new_image)


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

    # Create temporary surface to measure text
    temp_surface = cairo.ImageSurface(cairo.FORMAT_RGB24, 1, 1)
    temp_context = cairo.Context(temp_surface)
    try:
        layout = PangoCairo.create_layout(temp_context)
    except KeyError as e:
        if "could not find foreign type Context" in str(e):
            raise RuntimeError("Pango/Cairo not properly installed. See https://github.com/sign/WeLT/issues/31") from e

    # Set font
    font_desc = cached_font_description("sans", font_size)
    layout.set_font_description(font_desc)

    # Measure all texts to find maximum width
    layout.set_text(text, -1)
    text_width, text_height = layout.get_pixel_size()

    # Add padding and round up to nearest multiple of 32
    width = dim_to_block_size(text_width + 10, block_size=block_size)

    line_height = block_size

    # Create final surface
    surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, line_height)
    context = cairo.Context(surface)

    # Fill white background
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
    img_array = np.frombuffer(data, dtype=np.uint8).reshape((line_height, width, 4))
    img_array = img_array[:, :, 2::-1]  # Remove alpha channel + convert BGR→RGB

    return img_array.copy()


def render_text_image(text: str, block_size: int = 16, font_size: int = 12) -> Image.Image:
    img_array = render_text(text, block_size=block_size, font_size=font_size)
    return Image.fromarray(img_array)
