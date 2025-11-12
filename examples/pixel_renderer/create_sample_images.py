import argparse
import csv
import json
import os
import shutil
import sys
from importlib import metadata

from PIL import Image

from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS
from pixel_renderer import PixelRendererProcessor


def read_tsv(input_file):
    """Read TSV file into a list of dicts."""
    with open(input_file, encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        return list(reader)


def group_by_language(rows):
    """Group rows by language key."""
    grouped = {}
    for row in rows:
        lang = row["language"]
        grouped.setdefault(lang, []).append(row)
    return grouped


def create_language_image(lang, examples, pixel_processor, output_dir):
    """Render and concatenate text images for one language."""
    examples_sorted = sorted(examples, key=lambda x: int(x["index_id"]))

    rendered_images = []
    for ex in examples_sorted:
        text = ex.get("text", "").strip()
        if not text:
            continue
        img = pixel_processor.render_text_image(text)
        rendered_images.append(img)

    if not rendered_images:
        print(f"⚠️ No text rendered for {lang}")
        return

    widths = [im.width for im in rendered_images]
    heights = [im.height for im in rendered_images]
    total_height = sum(heights)
    max_width = max(widths)

    combined = Image.new("RGBA", (max_width, total_height), (255, 255, 255, 0))
    y_offset = 0
    for im in rendered_images:
        combined.paste(im, (0, y_offset))
        y_offset += im.height

    output_path = os.path.join(output_dir, f"{lang}.png")
    combined.save(output_path)
    print(f"✅ Saved {output_path}")


def get_versions():
    """Collect versions of relevant packages."""
    pkgs = [
        "pycairo",
        "pango",
        "cairo",
        "manimpango",
        "pixel_renderer",
        "pygobject",
        "gi",  # newly added
    ]
    versions = {}

    # Python package versions
    for pkg in pkgs:
        try:
            versions[pkg] = metadata.version(pkg)
        except metadata.PackageNotFoundError:
            versions[pkg] = None

    # Try native version lookups
    try:
        import cairo

        if hasattr(cairo, "cairo_version_string"):
            versions["cairo"] = cairo.cairo_version_string()
        elif hasattr(cairo, "version"):
            versions["cairo"] = cairo.version
    except ImportError:
        pass

    try:
        from gi.repository import Pango

        if hasattr(Pango, "version_string"):
            versions["pango"] = Pango.version_string()
    except ImportError:
        pass

    try:
        import gi

        if hasattr(gi, "__version__"):
            versions["gi"] = gi.__version__
    except ImportError:
        pass

    return versions


def write_versions_json(output_dir):
    versions = get_versions()
    version_path = os.path.join(output_dir, "versions.json")
    with open(version_path, "w", encoding="utf-8") as f:
        json.dump(versions, f, indent=2)
    print(f"📦 Saved version info to {version_path}")


def main():
    parser = argparse.ArgumentParser(description="Render grouped text images by language using PixelRenderer.")
    parser.add_argument("--input-file", required=True, help="Path to the TSV input file.")
    parser.add_argument("--output-dir", required=True, help="Directory to save output images.")
    args = parser.parse_args()

    # Validate output directory
    if os.path.exists(args.output_dir):
        print(f"❌ Error: Output directory '{args.output_dir}' already exists. Aborting.")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=False)
    shutil.copy2(args.input_file, os.path.join(args.output_dir, os.path.basename(args.input_file)))

    # Load TSV and group by language
    rows = read_tsv(args.input_file)
    grouped = group_by_language(rows)

    # Initialize renderer
    font_config = FontConfig(sources=FONTS_NOTO_SANS)
    pixel_processor = PixelRendererProcessor(font=font_config)

    # Render each language
    for lang, examples in grouped.items():
        create_language_image(lang, examples, pixel_processor, args.output_dir)

    # Record library versions
    write_versions_json(args.output_dir)

    print(f"\n🎉 All done! Images and metadata saved in '{args.output_dir}'")


if __name__ == "__main__":
    main()
