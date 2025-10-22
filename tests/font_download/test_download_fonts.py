"""Tests for font_download.download_fonts module."""

import json

import pytest

from font_download.download_fonts import _compute_sources_hash, download_fonts
from font_download.fonts import FontSource


class TestComputeSourcesHash:
    """Test _compute_sources_hash function."""

    def test_same_sources_same_hash(self):
        """Test identical sources produce same hash."""
        sources1 = [
            FontSource(url="https://example.com/a.ttf"),
            FontSource(url="https://example.com/b.ttf"),
        ]
        sources2 = [
            FontSource(url="https://example.com/a.ttf"),
            FontSource(url="https://example.com/b.ttf"),
        ]

        hash1 = _compute_sources_hash(sources1)
        hash2 = _compute_sources_hash(sources2)

        assert hash1 == hash2

    def test_different_order_same_hash(self):
        """Test sources in different order produce same hash (sorted internally)."""
        sources1 = [
            FontSource(url="https://example.com/a.ttf"),
            FontSource(url="https://example.com/b.ttf"),
        ]
        sources2 = [
            FontSource(url="https://example.com/b.ttf"),
            FontSource(url="https://example.com/a.ttf"),
        ]

        hash1 = _compute_sources_hash(sources1)
        hash2 = _compute_sources_hash(sources2)

        assert hash1 == hash2

    def test_different_sources_different_hash(self):
        """Test different sources produce different hash."""
        sources1 = [FontSource(url="https://example.com/a.ttf")]
        sources2 = [FontSource(url="https://example.com/b.ttf")]

        hash1 = _compute_sources_hash(sources1)
        hash2 = _compute_sources_hash(sources2)

        assert hash1 != hash2

    def test_hash_length(self):
        """Test hash is 16 characters."""
        sources = [FontSource(url="https://example.com/font.ttf")]

        hash_result = _compute_sources_hash(sources)

        assert len(hash_result) == 16


class TestDownloadFonts:
    """Test download_fonts function."""

    def test_downloads_and_creates_config(self, mock_download_setup, font_sources):
        """Test basic font download and config creation."""
        config_dir = download_fonts(font_sources)

        # Check config directory exists
        assert config_dir.exists()
        assert config_dir.is_dir()

        # Check font files exist (as symlinks)
        assert (config_dir / "font1.ttf").exists()
        assert (config_dir / "font2.ttf").exists()

        # Check sources.json exists
        assert (config_dir / "sources.json").exists()

        # Check fonts.conf exists
        assert (config_dir / "fonts.conf").exists()

    def test_sources_json_structure(self, mock_download_setup, font_sources):
        """Test sources.json has correct structure."""
        config_dir = download_fonts(font_sources)

        sources_json = json.loads((config_dir / "sources.json").read_text())

        assert len(sources_json) == 2
        assert sources_json[0]["name"] == "font1.ttf"
        assert sources_json[0]["url"] == "https://example.com/fonts/font1.ttf"
        assert "sha256" in sources_json[0]
        assert len(sources_json[0]["sha256"]) == 64

    def test_fontconfig_xml_structure(self, mock_download_setup, font_sources):
        """Test fonts.conf has correct XML structure."""
        config_dir = download_fonts(font_sources)

        fontconfig_content = (config_dir / "fonts.conf").read_text()

        assert '<?xml version="1.0"?>' in fontconfig_content
        assert 'DOCTYPE fontconfig SYSTEM "urn:fontconfig:fonts.dtd"' in fontconfig_content
        assert f"<dir>{config_dir}</dir>" in fontconfig_content
        assert "<fontconfig>" in fontconfig_content

    def test_reuses_existing_config(self, mock_download_setup, font_sources):
        """Test that same sources return existing config."""
        # First download
        config_dir1 = download_fonts(font_sources)
        mtime1 = (config_dir1 / "sources.json").stat().st_mtime

        # Second download with same sources
        config_dir2 = download_fonts(font_sources)
        mtime2 = (config_dir2 / "sources.json").stat().st_mtime

        # Should be same directory
        assert config_dir1 == config_dir2
        # sources.json should not have been recreated
        assert mtime1 == mtime2

    def test_fonts_are_symlinked(self, mock_download_setup, font_sources):
        """Test that fonts are symlinked from central cache."""
        config_dir = download_fonts(font_sources)

        font_symlink = config_dir / "font1.ttf"
        fonts_cache = mock_download_setup / "fonts" / "font1.ttf"

        assert font_symlink.is_symlink()
        assert fonts_cache.exists()
        assert font_symlink.resolve() == fonts_cache.resolve()

    def test_reuses_cached_fonts(self, mock_download_setup, font_sources):
        """Test that already cached fonts are not re-downloaded."""
        # Pre-create a font in cache
        fonts_cache = mock_download_setup / "fonts"
        fonts_cache.mkdir(parents=True, exist_ok=True)
        existing_font = fonts_cache / "font1.ttf"
        existing_font.write_bytes(b"existing-font-data")
        original_content = existing_font.read_bytes()

        # Download fonts
        config_dir = download_fonts(font_sources)

        # Font should not have been overwritten
        assert existing_font.read_bytes() == original_content
        assert (config_dir / "font1.ttf").exists()

    def test_different_sources_different_configs(self, mock_download_setup):
        """Test that different sources create different config dirs."""
        sources1 = [FontSource(url="https://example.com/font1.ttf")]
        sources2 = [FontSource(url="https://example.com/font2.ttf")]

        config_dir1 = download_fonts(sources1)
        config_dir2 = download_fonts(sources2)

        assert config_dir1 != config_dir2
        assert config_dir1.exists()
        assert config_dir2.exists()

    def test_handles_multiple_fonts(self, mock_download_setup):
        """Test downloading multiple fonts."""
        sources = [
            FontSource(url="https://example.com/font1.ttf"),
            FontSource(url="https://example.com/font2.ttf"),
            FontSource(url="https://example.com/font3.ttf"),
        ]

        config_dir = download_fonts(sources)

        assert (config_dir / "font1.ttf").exists()
        assert (config_dir / "font2.ttf").exists()
        assert (config_dir / "font3.ttf").exists()

        sources_json = json.loads((config_dir / "sources.json").read_text())
        assert len(sources_json) == 3
