import json

import pytest
from PIL import Image, ImageChops

from tests.pixel_renderer.regression.create_sample_images import (
    ASSETS_DIR,
    SAMPLES_TSV,
    build_processor,
    get_versions,
    group_by_language,
    read_tsv,
    render_language_image,
)

EXAMPLES_BY_LANGUAGE = group_by_language(read_tsv(SAMPLES_TSV))

# Pixel-exact comparison only holds when the libraries that shape glyphs match
# the ones used to generate the reference images.
RENDERING_STACK_KEYS = ("pango", "cairo")


@pytest.fixture(scope="session")
def pixel_processor():
    reference = json.loads((ASSETS_DIR / "versions.json").read_text())
    current = get_versions()
    drift = {k: f"{reference[k]} -> {current[k]}" for k in RENDERING_STACK_KEYS if reference[k] != current[k]}
    if drift:
        pytest.skip(f"Rendering stack differs from reference images ({drift}); regenerate with create_sample_images.py")
    return build_processor()


def image_mismatch(rendered, reference):
    """Describe how the images differ, or return None if they are identical."""
    if rendered.size != reference.size:
        return f"size {rendered.size} != reference size {reference.size}"
    bbox = ImageChops.difference(rendered, reference).getbbox()
    if bbox:
        return f"pixels differ within bbox {bbox}"
    return None


@pytest.mark.parametrize("lang", sorted(EXAMPLES_BY_LANGUAGE))
def test_render_matches_reference(lang, pixel_processor):
    """Compare re-rendered language images with the committed reference ones."""
    reference_path = ASSETS_DIR / f"{lang}.png"
    assert reference_path.exists(), f"Reference image missing: {reference_path}"

    rendered_img = render_language_image(EXAMPLES_BY_LANGUAGE[lang], pixel_processor)
    assert rendered_img is not None, f"No valid examples for {lang}"

    ref_img = Image.open(reference_path).convert("RGBA")
    mismatch = image_mismatch(rendered_img, ref_img)
    assert mismatch is None, f"Rendered image differs from reference for {lang}: {mismatch}"
