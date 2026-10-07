import subprocess
import sys

FREETYPE_VERSION = "from PIL import ImageFont, features; print(features.version('freetype2'))"


def freetype_version_after(setup: str) -> str:
    code = f"{setup}\n{FREETYPE_VERSION}"
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout.strip()


def test_pillow_keeps_its_own_freetype_after_importing_pixel_renderer():
    """Pillow must not bind to the system FreeType loaded by Pango (issue #16)."""
    assert freetype_version_after("import pixel_renderer") == freetype_version_after("")
