import concurrent.futures
import hashlib
import json
import logging
import os
from pathlib import Path
from urllib.request import urlretrieve

from platformdirs import user_cache_dir

from font_download.fonts import FontEntity, FontsSources

FONT_DOWNLOAD_CACHE_DIR = Path(user_cache_dir("font_download"))


def _compute_sources_hash(sources: FontsSources) -> str:
    """Compute unique hash from sorted source URLs."""
    urls = sorted(source.url for source in sources)
    combined = "\n".join(urls).encode("utf-8")
    return hashlib.sha256(combined).hexdigest()[:16]


def create_fontconfig_xml(config_dir: Path) -> None:
    """Create fontconfig XML file pointing to the config directory."""
    xml_content = f"""<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd">
<fontconfig>
    <dir>{config_dir}</dir>
</fontconfig>
"""
    (config_dir / "fonts.conf").write_text(xml_content, encoding="utf-8")


def download_fonts(sources: FontsSources, max_workers: int | None = None) -> Path:
    """Download fonts and create a fontconfig configuration directory.

    Steps:
    1. Downloads fonts to FONTDOWNLOAD_CACHE_DIR/"fonts" (validates SHA256)
    2. Creates unique config dir based on hash of sources
    3. Writes sources.json with font metadata
    4. Symlinks fonts from cache to config dir
    5. Creates fonts.conf fontconfig XML

    Args:
        sources: List of FontSource objects to download
        max_workers: Maximum parallel downloads

    Returns:
        Path to config directory
    """
    fonts_cache_dir = FONT_DOWNLOAD_CACHE_DIR / "fonts"
    fonts_cache_dir.mkdir(parents=True, exist_ok=True)

    config_base_dir = FONT_DOWNLOAD_CACHE_DIR / "config"
    config_hash = _compute_sources_hash(sources)
    config_dir = config_base_dir / config_hash

    # Return existing config if valid
    if (config_dir / "sources.json").exists():
        return config_dir

    config_dir.mkdir(parents=True, exist_ok=True)

    def download_font_task(source):
        """Download font and return metadata."""
        font_path = fonts_cache_dir / source.name

        # Download if doesn't exist
        if not font_path.exists():
            logging.info(f"Downloading {source.name}...")
            urlretrieve(source.url, font_path)

        # Create symlink in config dir
        symlink_path = config_dir / source.name
        # Remove existing symlink if it exists (handles broken symlinks)
        if symlink_path.is_symlink() or symlink_path.exists():
            symlink_path.unlink(missing_ok=True)
        symlink_path.symlink_to(font_path)

        return FontEntity(name=source.name, url=source.url, file_path=font_path)

    # Download in parallel
    max_workers = max_workers or os.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        font_metadata = list(executor.map(download_font_task, sources))

    # Write sources.json
    font_metadata = [font.to_dict() for font in font_metadata]
    (config_dir / "sources.json").write_text(json.dumps(font_metadata, indent=2), encoding="utf-8")

    # Create fontconfig XML
    create_fontconfig_xml(config_dir)

    return config_dir
