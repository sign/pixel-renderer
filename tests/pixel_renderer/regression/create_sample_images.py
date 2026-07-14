import argparse
import csv
import json
from importlib import metadata
from pathlib import Path

from PIL import Image

from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS
from pixel_renderer import PixelRendererProcessor

REGRESSION_DIR = Path(__file__).parent
SAMPLES_TSV = REGRESSION_DIR / "samples.tsv"
ASSETS_DIR = REGRESSION_DIR / "assets"


def read_tsv(input_file):
    with open(input_file, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def group_by_language(rows):
    grouped = {}
    for row in rows:
        lang = row["language"]
        grouped.setdefault(lang, []).append(row)
    return grouped


def build_processor():
    """Single source of truth for the rendering configuration used by both generation and tests."""
    return PixelRendererProcessor(font=FontConfig(sources=FONTS_NOTO_SANS))


def render_language_image(examples, pixel_processor):
    """Render each example and concatenate them vertically into one image."""
    examples_sorted = sorted(examples, key=lambda x: int(x["index_id"]))

    rendered_images = []
    for ex in examples_sorted:
        text = ex["text"].strip()
        if not text:
            continue
        img = pixel_processor.render_text_image(text)
        rendered_images.append(img)

    if not rendered_images:
        return None

    total_height = sum(im.height for im in rendered_images)
    max_width = max(im.width for im in rendered_images)

    combined = Image.new("RGBA", (max_width, total_height), (255, 255, 255, 0))
    y_offset = 0
    for im in rendered_images:
        combined.paste(im, (0, y_offset))
        y_offset += im.height

    return combined


def get_versions():
    """Collect versions of the packages that affect rendering output."""
    # Imported here so import order stays irrelevant: importing pixel_renderer above
    # already ran gi.require_version, which gi.repository.Pango needs.
    import cairo
    import gi
    from gi.repository import Pango

    return {
        "pixel_renderer": metadata.version("pixel_renderer"),
        "pycairo": metadata.version("pycairo"),
        "pygobject": metadata.version("pygobject"),
        "gi": gi.__version__,
        "cairo": cairo.cairo_version_string(),
        "pango": Pango.version_string(),
    }


def write_versions_json(output_dir):
    versions = get_versions()
    version_path = output_dir / "versions.json"
    with open(version_path, "w", encoding="utf-8") as f:
        json.dump(versions, f, indent=2)
    print(f"📦 Saved version info to {version_path}")


def main():
    parser = argparse.ArgumentParser(description="Render the reference images used by the regression tests.")
    parser.add_argument("--input-file", type=Path, default=SAMPLES_TSV, help="Path to the TSV input file.")
    parser.add_argument("--output-dir", type=Path, default=ASSETS_DIR, help="Directory to save output images.")
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = read_tsv(args.input_file)
    grouped = group_by_language(rows)

    pixel_processor = build_processor()

    for lang, examples in grouped.items():
        combined = render_language_image(examples, pixel_processor)
        if combined is None:
            print(f"⚠️ No text rendered for {lang}")
            continue
        output_path = args.output_dir / f"{lang}.png"
        combined.save(output_path)
        print(f"✅ Saved {output_path}")

    write_versions_json(args.output_dir)

    print(f"\n🎉 All done! Images and metadata saved in '{args.output_dir}'")


if __name__ == "__main__":
    main()
