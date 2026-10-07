import subprocess
import sys

import pytest

FREETYPE_VERSION = "from PIL import ImageFont, features; print(features.version('freetype2'))"


def freetype_version_after(setup: str) -> str:
    code = f"{setup}\n{FREETYPE_VERSION}"
    return subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True).stdout.strip()


@pytest.mark.parametrize("module", ["pixel_renderer", "pixel_renderer.renderer", "font_configurator.font_configurator"])
def test_pillow_keeps_its_own_freetype(module):
    """Pillow must not bind to the system FreeType loaded by Pango (issue #16)."""
    assert freetype_version_after(f"import {module}") == freetype_version_after("")
