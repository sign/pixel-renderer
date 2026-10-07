# Load Pillow's FreeType bindings before anything imports gi.repository.Pango.
# Pango is loaded with RTLD_GLOBAL, so if it comes first, Pillow's bundled FreeType/HarfBuzz
# resolve their symbols against the system libraries instead, corrupting SignWriting rendering.
# See https://github.com/sign/pixel-renderer/issues/16
from PIL import ImageFont  # noqa: F401, I001

from pixel_renderer.processor import PixelRendererProcessor  # noqa: F401
from pixel_renderer.renderer import *  # noqa: F403
