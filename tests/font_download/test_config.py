"""Tests for FontConfig."""

import json
import tempfile

from font_download import FontConfig
from font_download.fonts import FontSource


class TestFontConfig:
    """Test FontConfig class."""

    def test_config_initialization(self, mock_download_setup, font_sources):
        """Test FontConfig can be initialized."""
        config = FontConfig(sources=font_sources)
        font_dir = config.get_font_dir()

        assert font_dir.exists()
        assert (font_dir / "sources.json").exists()

    def test_config_to_dict(self, mock_download_setup, font_sources):
        """Test FontConfig.to_dict() serialization."""
        config = FontConfig(sources=font_sources)

        result = config.to_dict()

        assert "sources" in result
        assert isinstance(result["sources"], list)
        assert len(result["sources"]) == 2
        assert result["sources"][0]["name"] == "font1.ttf"
        assert result["sources"][0]["url"] == "https://example.com/fonts/font1.ttf"

    def test_config_save_and_load_pretrained(self, mock_download_setup, font_sources):
        """Test save_pretrained and from_pretrained workflow."""
        config = FontConfig(sources=font_sources)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Save config
            config.save_pretrained(save_directory=temp_dir, push_to_hub=False)

            # Load config
            new_config = FontConfig.from_pretrained(temp_dir)
            new_font_dir = new_config.get_font_dir()

            # Verify loaded config
            assert new_font_dir.exists()
            assert (new_font_dir / "sources.json").exists()

            # Verify sources match
            original_sources = config.to_dict()["sources"]
            loaded_sources = new_config.to_dict()["sources"]
            assert len(original_sources) == len(loaded_sources)
            assert original_sources[0]["name"] == loaded_sources[0]["name"]
            assert original_sources[0]["url"] == loaded_sources[0]["url"]

    def test_config_has_no_render_methods(self, mock_download_setup, font_sources):
        """Test that FontConfig does not have render methods (removed from simplified version)."""
        config = FontConfig(sources=font_sources)

        # Config should not have render methods
        assert not hasattr(config, "render_text")
        assert not hasattr(config, "render_text_image")

    def test_config_class_attributes(self):
        """Test FontConfig class attributes."""
        assert FontConfig.model_type == "font_config"

    def test_config_with_single_font(self, mock_download_setup):
        """Test config with single font source."""
        sources = [FontSource(url="https://example.com/single.ttf")]

        config = FontConfig(sources=sources)

        result = config.to_dict()
        assert len(result["sources"]) == 1
        assert result["sources"][0]["name"] == "single.ttf"

    def test_config_persists_font_metadata(self, mock_download_setup, font_sources):
        """Test that font metadata (URLs, names, hashes) are persisted."""
        config = FontConfig(sources=font_sources)

        # Read sources.json directly
        sources_json = json.loads((config.get_font_dir() / "sources.json").read_text())

        # Verify all metadata is present
        for source in sources_json:
            assert "name" in source
            assert "url" in source
            assert "sha256" in source
            assert source["name"].endswith(".ttf")
            assert source["url"].startswith("https://")
            assert len(source["sha256"]) == 64

    def test_config_dir_structure(self, mock_download_setup, font_sources):
        """Test that config directory has expected structure."""
        config = FontConfig(sources=font_sources)

        # Check directory structure
        font_dir = config.get_font_dir()
        assert font_dir.is_dir()
        assert (font_dir / "sources.json").is_file()
        assert (font_dir / "fonts.conf").is_file()
        assert (font_dir / "font1.ttf").exists()
        assert (font_dir / "font2.ttf").exists()
