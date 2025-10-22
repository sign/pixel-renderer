import csv
import os

import pytest
from PIL import Image, ImageChops

from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS
from pixel_renderer import PixelRendererProcessor

# ---------------------------
#  Fixtures
# ---------------------------


@pytest.fixture(scope="session")
def sample_images_dir():
    """
    Directory that contains {lang}.png reference images and samples.tsv.
    Taken from the SAMPLE_IMAGES_DIR environment variable.
    If unset, all tests will be skipped.
    """
    path = os.environ.get("SAMPLE_IMAGES_DIR")
    if not path:
        pytest.skip("Environment variable SAMPLE_IMAGES_DIR not set — skipping visual tests")
    if not os.path.exists(path):
        pytest.skip(f"SAMPLE_IMAGES_DIR path not found: {path}")
    return path


# ---------------------------
#  Utility helpers
# ---------------------------


def read_tsv(tsv_path):
    with open(tsv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def group_by_language(rows):
    grouped = {}
    for row in rows:
        lang = row["language"]
        grouped.setdefault(lang, []).append(row)
    return grouped


def render_language_image(lang, examples, pixel_processor):
    """Render and concatenate text examples for one language."""
    examples_sorted = sorted(examples, key=lambda x: int(x["index_id"]))
    rendered_images = []

    for ex in examples_sorted:
        text = ex.get("text", "").strip()
        if not text:
            continue
        img = pixel_processor.render_text_image(text)
        rendered_images.append(img)

    if not rendered_images:
        pytest.skip(f"No valid examples for {lang}")

    widths = [im.width for im in rendered_images]
    heights = [im.height for im in rendered_images]
    total_height = sum(heights)
    max_width = max(widths)

    combined = Image.new("RGBA", (max_width, total_height), (255, 255, 255, 0))
    y_offset = 0
    for im in rendered_images:
        combined.paste(im, (0, y_offset))
        y_offset += im.height

    return combined


def images_are_equal(img1, img2):
    """Compare two images pixel-by-pixel."""
    if img1.size != img2.size:
        return False
    diff = ImageChops.difference(img1, img2)
    return diff.getbbox() is None


# ---------------------------
#  Dynamic test generation
# ---------------------------


def pytest_generate_tests(metafunc):
    """Dynamically create one test per language if SAMPLE_IMAGES_DIR is set."""
    if "language_case" in metafunc.fixturenames:
        base_dir = os.environ.get("SAMPLE_IMAGES_DIR")
        if not base_dir or not os.path.exists(base_dir):
            metafunc.parametrize("language_case", [])
            return

        tsv_path = os.path.join(base_dir, "samples.tsv")
        if not os.path.exists(tsv_path):
            pytest.skip(f"No samples.tsv found in {base_dir}")

        rows = read_tsv(tsv_path)
        grouped = group_by_language(rows)
        cases = [(lang, examples) for lang, examples in grouped.items()]
        metafunc.parametrize("language_case", cases, ids=[c[0] for c in cases])


# ---------------------------
#  Tests
# ---------------------------


def test_render_matches_reference(language_case, sample_images_dir):
    """Compare re-rendered language images with reference ones."""
    lang, examples = language_case
    reference_path = os.path.join(sample_images_dir, f"{lang}.png")
    if not os.path.exists(reference_path):
        pytest.skip(f"Reference image missing: {reference_path}")

    font_config = FontConfig(sources=FONTS_NOTO_SANS)
    pixel_processor = PixelRendererProcessor(font=font_config)

    rendered_img = render_language_image(lang, examples, pixel_processor)
    ref_img = Image.open(reference_path).convert("RGBA")

    assert images_are_equal(rendered_img, ref_img), f"Rendered image differs from reference for {lang}"
