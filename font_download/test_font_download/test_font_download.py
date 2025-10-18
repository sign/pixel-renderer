import json
import pathlib
from unittest.mock import Mock, patch

import pytest
import requests  # type: ignore[import-untyped]

from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.tools import FontEntity, FontSource


class TestReproducibleFontDownloadInit:
    """Test initialization and cache directory creation."""

    def test_init_with_string_path(self, tmp_path: pathlib.Path) -> None:
        """Test initialization with string path."""
        downloader = ReproducibleFontDownload(cache_dir=str(tmp_path))

        assert downloader.cache_dir == tmp_path
        assert downloader.cache_dir.exists()
        assert downloader.configs_dir.exists()
        assert downloader.configs_dir == tmp_path.joinpath("configs")

    def test_init_with_pathlib_path(self, tmp_path: pathlib.Path) -> None:
        """Test initialization with pathlib.Path."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        assert downloader.cache_dir == tmp_path
        assert downloader.cache_dir.exists()

    def test_cache_dir_created_if_not_exists(self, tmp_path: pathlib.Path) -> None:
        """Test that cache directory is created if it doesn't exist."""
        cache_dir = tmp_path.joinpath("new_cache_dir")
        assert not cache_dir.exists()

        downloader = ReproducibleFontDownload(cache_dir=cache_dir)

        assert cache_dir.exists()
        assert downloader.cache_dir == cache_dir


class TestSaveConfig:
    """Test save_config functionality."""

    def test_save_config_basic(
        self, tmp_path: pathlib.Path, font_sources: list[FontSource], fake_download: None
    ) -> None:
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)
        config_path = downloader.save_config(sources=font_sources, config_name="test_fonts")

        assert config_path.exists()
        fonts_dir = tmp_path.joinpath("test_fonts")
        assert fonts_dir.exists()

        # All fonts should have been "downloaded" by fake_download
        for source in font_sources:
            assert fonts_dir.joinpath(source.name).exists()

    def test_save_config_creates_json(
        self, tmp_path: pathlib.Path, font_sources: list[FontSource], fake_download: None, mock_fonts: list[FontEntity]
    ) -> None:
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)
        config_path = downloader.save_config(sources=font_sources, config_name="test_fonts")

        data = json.loads(config_path.read_text())
        assert len(data) == len(font_sources)
        for font_entry in data:
            assert set(font_entry.keys()) == {"name", "url", "sha256"}

    def test_save_config_custom_dest_dir(
        self, tmp_path: pathlib.Path, font_sources: list[FontSource], fake_download: None
    ) -> None:
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)
        custom_dir = tmp_path.joinpath("custom_configs")
        config_path = downloader.save_config(sources=font_sources, config_name="test_fonts", dest_dir=custom_dir)

        assert config_path.parent == custom_dir
        assert config_path.exists()

    def test_save_config_no_fonts_downloaded_raises_error(
        self, tmp_path: pathlib.Path, font_sources: list[FontSource]
    ) -> None:
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)
        with patch.object(downloader, "_download_file", return_value=False):
            with pytest.raises(RuntimeError, match="No fonts were successfully downloaded"):
                downloader.save_config(sources=font_sources, config_name="test_fonts")

    def test_save_config_partial_download_success(self, tmp_path: pathlib.Path, font_sources: list[FontSource]) -> None:
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # custom fake download that writes files only for the first call
        def fake_download(url: str, dest_path: pathlib.Path) -> bool:
            if "font1.ttf" in url:
                dest_path.write_bytes(b"fake font data")  # simulate a successful download
                return True
            return False

        with patch.object(downloader, "_download_file", side_effect=fake_download):
            config_path = downloader.save_config(sources=font_sources, config_name="test_fonts")

        data = json.loads(config_path.read_text())
        assert len(data) == 1  # only one font succeeded


class TestFromConfig:
    """Test from_config functionality."""

    def test_from_config_by_name(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test loading fonts by config name."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # First, create a config
        downloader.save_config(sources=font_sources, config_name="test_fonts")

        # Clear fonts to test re-download
        fonts_dir = tmp_path.joinpath("test_fonts")
        for font_file in fonts_dir.glob("*.ttf"):
            font_file.unlink()

        # Load from config by name
        result_dir = downloader.from_config("test_fonts")

        assert result_dir == fonts_dir
        assert result_dir.exists()

        # Verify all fonts were downloaded
        for source in font_sources:
            assert result_dir.joinpath(source.name).exists()

    def test_from_config_by_path(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test loading fonts by config path."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        config_path = downloader.save_config(sources=font_sources, config_name="test_fonts")

        # Load from config by path
        result_dir = downloader.from_config(config_path)

        assert result_dir.exists()
        for source in font_sources:
            assert result_dir.joinpath(source.name).exists()

    def test_from_config_uses_cached_fonts(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that existing valid fonts are not re-downloaded."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config and download fonts
        downloader.save_config(sources=font_sources, config_name="test_fonts")

        # Track if download is called
        with patch.object(downloader, "_download_file") as mock_download:
            result_dir = downloader.from_config("test_fonts")

            # Should not download since fonts exist
            mock_download.assert_not_called()

        assert result_dir.exists()

    def test_from_config_force_download(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test force_download parameter re-downloads all fonts."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config
        downloader.save_config(sources=font_sources, config_name="test_fonts")

        # Track downloads
        with patch.object(downloader, "_download_file", return_value=True) as mock_download:
            result_dir = downloader.from_config("test_fonts", force_download=True)  # noqa: F841

            # Should download all fonts
            assert mock_download.call_count == len(font_sources)

    def test_from_config_integrity_check_passes(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that integrity check passes for valid fonts."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config with fonts
        downloader.save_config(sources=font_sources, config_name="test_fonts")

        # Load again - should verify integrity and not re-download
        with patch.object(downloader, "_download_file") as mock_download:
            result_dir = downloader.from_config("test_fonts")  # noqa: F841
            mock_download.assert_not_called()

    def test_from_config_integrity_check_fails_redownloads(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that corrupted fonts are re-downloaded."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config
        config_path = downloader.save_config(sources=font_sources, config_name="test_fonts")  # noqa: F841

        # Corrupt one font file
        fonts_dir = tmp_path.joinpath("test_fonts")
        first_font = fonts_dir.joinpath(font_sources[0].name)
        first_font.write_bytes(b"corrupted content")

        # Load from config - should detect corruption and re-download
        result_dir = downloader.from_config("test_fonts")  # noqa: F841

        # Verify font was re-downloaded (hash should match now)
        assert first_font.exists()

    def test_from_config_missing_config_raises_error(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test that FileNotFoundError is raised for missing config."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        with pytest.raises(FileNotFoundError):
            downloader.from_config("nonexistent_config")

    def test_from_config_invalid_json_raises_error(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test that JSONDecodeError is raised for invalid JSON."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create invalid JSON config
        config_path = downloader.configs_dir.joinpath("invalid.json")
        config_path.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            downloader.from_config("invalid")


class TestClearCache:
    """Test cache clearing functionality."""

    def test_clear_cache_specific_config(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test clearing cache for a specific config."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create two configs
        downloader.save_config(sources=font_sources, config_name="fonts1")
        downloader.save_config(sources=font_sources, config_name="fonts2")

        fonts1_dir = tmp_path.joinpath("fonts1")
        fonts2_dir = tmp_path.joinpath("fonts2")

        assert fonts1_dir.exists()
        assert fonts2_dir.exists()

        # Clear only fonts1
        downloader.clear_cache(config_name="fonts1")

        assert not fonts1_dir.exists()
        assert fonts2_dir.exists()

    def test_clear_cache_all_fonts(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test clearing all fonts cache."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create multiple configs
        downloader.save_config(sources=font_sources, config_name="fonts1")
        downloader.save_config(sources=font_sources, config_name="fonts2")

        fonts1_dir = tmp_path.joinpath("fonts1")
        fonts2_dir = tmp_path.joinpath("fonts2")
        config1 = downloader.configs_dir.joinpath("fonts1.json")
        config2 = downloader.configs_dir.joinpath("fonts2.json")

        # Clear all fonts
        downloader.clear_cache()

        # Fonts should be gone
        assert not fonts1_dir.exists()
        assert not fonts2_dir.exists()

        # Configs should still exist
        assert config1.exists()
        assert config2.exists()

    def test_clear_cache_with_remove_configs(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test clearing cache including config files."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create configs
        downloader.save_config(sources=font_sources, config_name="fonts1")
        downloader.save_config(sources=font_sources, config_name="fonts2")

        fonts1_dir = tmp_path.joinpath("fonts1")
        config1 = downloader.configs_dir.joinpath("fonts1.json")

        # Clear everything
        downloader.clear_cache(remove_configs=True)

        # Everything should be gone
        assert not fonts1_dir.exists()
        assert not config1.exists()

        # Configs dir should still exist (recreated)
        assert downloader.configs_dir.exists()

    def test_clear_cache_specific_with_remove_config(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test clearing specific config with its config file."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create two configs
        downloader.save_config(sources=font_sources, config_name="fonts1")
        downloader.save_config(sources=font_sources, config_name="fonts2")

        fonts1_dir = tmp_path.joinpath("fonts1")
        fonts2_dir = tmp_path.joinpath("fonts2")
        config1 = downloader.configs_dir.joinpath("fonts1.json")
        config2 = downloader.configs_dir.joinpath("fonts2.json")

        # Clear only fonts1 with config
        downloader.clear_cache(config_name="fonts1", remove_configs=True)

        # fonts1 and its config should be gone
        assert not fonts1_dir.exists()
        assert not config1.exists()

        # fonts2 should remain
        assert fonts2_dir.exists()
        assert config2.exists()

    def test_clear_cache_nonexistent_config(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test clearing cache for nonexistent config (should not raise error)."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Should not raise error
        downloader.clear_cache(config_name="nonexistent")


class TestListConfigs:
    """Test config listing functionality."""

    def test_list_configs_empty(self, tmp_path: pathlib.Path) -> None:
        """Test listing configs when none exist."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        configs = downloader.list_configs()

        assert configs == []

    def test_list_configs_multiple(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test listing multiple configs."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create multiple configs
        downloader.save_config(sources=font_sources, config_name="fonts_a")
        downloader.save_config(sources=font_sources, config_name="fonts_b")
        downloader.save_config(sources=font_sources, config_name="fonts_c")

        configs = downloader.list_configs()

        assert len(configs) == 3
        assert configs == ["fonts_a", "fonts_b", "fonts_c"]  # Should be sorted

    def test_list_configs_sorted(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that configs are returned in sorted order."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create in random order
        downloader.save_config(sources=font_sources, config_name="zebra")
        downloader.save_config(sources=font_sources, config_name="alpha")
        downloader.save_config(sources=font_sources, config_name="beta")

        configs = downloader.list_configs()

        assert configs == ["alpha", "beta", "zebra"]


class TestFromSources:
    """Test from_sources class method."""

    def test_from_sources_basic(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test from_sources creates config and returns fonts directory."""
        fonts_dir = ReproducibleFontDownload.from_sources(
            sources=font_sources,
            config_name="test_fonts",
            cache_dir=tmp_path,
        )

        assert fonts_dir.exists()
        assert fonts_dir == tmp_path.joinpath("test_fonts")

        # Verify fonts exist
        for source in font_sources:
            assert fonts_dir.joinpath(source.name).exists()

        # Verify config exists
        config_path = tmp_path.joinpath("configs").joinpath("test_fonts.json")
        assert config_path.exists()

    def test_from_sources_returns_correct_path(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that from_sources returns the correct fonts directory path."""
        result = ReproducibleFontDownload.from_sources(
            sources=font_sources,
            config_name="my_fonts",
            cache_dir=tmp_path,
        )

        assert isinstance(result, pathlib.Path)
        assert result.name == "my_fonts"


class TestDownloadFile:
    """Test _download_file private method."""

    def test_download_file_success(
        self,
        tmp_path: pathlib.Path,
        mock_fonts: list[FontEntity],
    ) -> None:
        """Test successful file download."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        dest_path = tmp_path.joinpath("test_font.ttf")

        with patch("requests.get") as mock_get:
            mock_response = Mock()
            mock_response.iter_content = Mock(return_value=[b"fake font data"])
            mock_response.raise_for_status = Mock()
            mock_response.__enter__ = Mock(return_value=mock_response)
            mock_response.__exit__ = Mock(return_value=False)
            mock_get.return_value = mock_response

            result = downloader._download_file(url=mock_fonts[0].url, dest_path=dest_path)

        assert result is True
        assert dest_path.exists()

    def test_download_file_failure(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test failed file download."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        dest_path = tmp_path.joinpath("test_font.ttf")

        with patch("requests.get", side_effect=requests.RequestException("Network error")):
            result = downloader._download_file(url="https://example.com/font.ttf", dest_path=dest_path)

        assert result is False
        assert not dest_path.exists()

    def test_download_file_cleans_incomplete_file(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test that incomplete files are removed on failure."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        dest_path = tmp_path.joinpath("test_font.ttf")

        # Create a partial file
        dest_path.write_bytes(b"partial data")

        with patch("requests.get", side_effect=requests.RequestException("Network error")):
            result = downloader._download_file(url="https://example.com/font.ttf", dest_path=dest_path)

        assert result is False
        assert not dest_path.exists()


class TestIntegrityVerification:
    """Test font integrity verification."""

    def test_verify_font_integrity_success(
        self,
        tmp_path: pathlib.Path,
        mock_fonts: list[FontEntity],
    ) -> None:
        """Test successful integrity verification."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        font_path = tmp_path.joinpath(mock_fonts[0].name)
        font_path.write_bytes(f"mock-font-content-{mock_fonts[0].name}".encode())

        result = downloader._verify_font_integrity(font_path=font_path, expected_sha256=mock_fonts[0].sha256)

        assert result is True

    def test_verify_font_integrity_failure(
        self,
        tmp_path: pathlib.Path,
        mock_fonts: list[FontEntity],
    ) -> None:
        """Test failed integrity verification."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        font_path = tmp_path.joinpath(mock_fonts[0].name)
        font_path.write_bytes(b"wrong content")

        result = downloader._verify_font_integrity(font_path=font_path, expected_sha256=mock_fonts[0].sha256)

        assert result is False

    def test_verify_font_integrity_missing_file(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test integrity verification with missing file."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        font_path = tmp_path.joinpath("nonexistent.ttf")

        result = downloader._verify_font_integrity(font_path=font_path, expected_sha256="dummy_hash")

        assert result is False


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_sources_list(
        self,
        tmp_path: pathlib.Path,
    ) -> None:
        """Test handling of empty sources list."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        with pytest.raises(RuntimeError, match="No fonts were successfully downloaded"):
            downloader.save_config(sources=[], config_name="empty")

    def test_config_with_missing_sha256(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test loading config that has no SHA256 field (backward compatibility)."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config manually without SHA256
        config_path = downloader.configs_dir.joinpath("no_sha.json")
        config_data = [
            {
                "name": source.name,
                "url": source.url,
                # No sha256 field
            }
            for source in font_sources
        ]
        with config_path.open("w") as f:
            json.dump(config_data, f)

        # Should still work (downloads fonts)
        fonts_dir = downloader.from_config("no_sha")

        assert fonts_dir.exists()
        for source in font_sources:
            assert fonts_dir.joinpath(source.name).exists()

    def test_malformed_config_entry_skipped(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that malformed config entries are skipped."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config with one malformed entry
        config_path = downloader.configs_dir.joinpath("malformed.json")
        config_data = [
            {"name": font_sources[0].name, "url": font_sources[0].url},
            {"invalid": "entry"},  # Malformed
            {"name": font_sources[1].name, "url": font_sources[1].url},
        ]
        with config_path.open("w") as f:
            json.dump(config_data, f)

        # Should process valid entries and skip malformed
        fonts_dir = downloader.from_config("malformed")

        assert fonts_dir.joinpath(font_sources[0].name).exists()
        assert fonts_dir.joinpath(font_sources[1].name).exists()

    def test_special_characters_in_config_name(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test config names with special characters."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        config_name = "my-fonts_v2-1"
        config_path = downloader.save_config(sources=font_sources, config_name=config_name)

        assert config_path.exists()
        assert config_path.name == f"{config_name}.json"  # Check full filename instead of stem

        # Should be able to load it
        fonts_dir = downloader.from_config(config_name)
        assert fonts_dir.exists()
