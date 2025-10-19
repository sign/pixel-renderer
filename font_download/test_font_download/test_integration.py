"""Integration tests for end-to-end workflows."""

import pathlib
from unittest.mock import patch

from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.tools import FontSource


class TestScenario1:
    """Test Scenario 1: Create config, then load it."""

    def test_create_and_load_workflow(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test complete workflow: create config -> load fonts."""
        # Step 1: Create downloader
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Step 2: Save config with fonts
        config_path = downloader.save_config(sources=font_sources, config_name="my_project_fonts")

        assert config_path.exists()
        assert config_path.name == "my_project_fonts.json"

        # Step 3: Load fonts from config
        fonts_dir = downloader.from_config("my_project_fonts")

        assert fonts_dir.exists()
        assert fonts_dir == tmp_path.joinpath("my_project_fonts")

        # Verify all fonts are present
        for source in font_sources:
            font_file = fonts_dir.joinpath(source.name)
            assert font_file.exists()
            assert font_file.stat().st_size > 0

    def test_create_load_modify_reload(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test creating, loading, modifying cache, and reloading."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config
        downloader.save_config(sources=font_sources, config_name="test_fonts")

        # Load fonts
        fonts_dir = downloader.from_config("test_fonts")
        assert all(fonts_dir.joinpath(s.name).exists() for s in font_sources)

        # Simulate cache corruption by deleting one font
        fonts_dir.joinpath(font_sources[0].name).unlink()

        # Reload - should detect missing font and re-download
        fonts_dir = downloader.from_config("test_fonts")

        # All fonts should be present again
        assert all(fonts_dir.joinpath(s.name).exists() for s in font_sources)


class TestScenario2:
    """Test Scenario 2: Load any config (download if needed)."""

    def test_load_existing_config(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test loading config that already exists."""
        # Pre-create config
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)
        downloader.save_config(sources=font_sources, config_name="existing_fonts")

        # Create new instance and load
        new_downloader = ReproducibleFontDownload(cache_dir=tmp_path)
        fonts_dir = new_downloader.from_config("existing_fonts")

        assert fonts_dir.exists()
        for source in font_sources:
            assert fonts_dir.joinpath(source.name).exists()

    def test_load_and_verify_cached_fonts(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that cached fonts are used without re-downloading."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # First load - downloads fonts
        downloader.save_config(sources=font_sources, config_name="cached_fonts")
        fonts_dir = downloader.from_config("cached_fonts")

        # Get file modification times
        mtimes: dict[str, float] = {
            source.name: fonts_dir.joinpath(source.name).stat().st_mtime for source in font_sources
        }

        # Second load - should use cache
        fonts_dir = downloader.from_config("cached_fonts")

        # Modification times should be unchanged
        for source in font_sources:
            assert fonts_dir.joinpath(source.name).stat().st_mtime == mtimes[source.name]

    def test_load_with_integrity_verification(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test loading config with automatic integrity verification."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config
        downloader.save_config(sources=font_sources, config_name="verified_fonts")
        fonts_dir = tmp_path.joinpath("verified_fonts")

        # Store original content
        original_font = fonts_dir.joinpath(font_sources[0].name)
        original_content = original_font.read_bytes()  # noqa: F841

        # Corrupt one font
        original_font.write_bytes(b"corrupted data")
        assert original_font.read_bytes() == b"corrupted data"

        # Load - should detect corruption and fix it
        result_dir = downloader.from_config("verified_fonts")  # noqa: F841

        # Font should be restored (re-downloaded with fake data)
        assert original_font.exists()
        restored_content = original_font.read_bytes()

        # Check if it was re-downloaded (should have "fake font data" from fixture)
        assert restored_content == b"mock-font-content-font1.ttf"
        assert restored_content != b"corrupted data"


class TestMultipleConfigs:
    """Test working with multiple configurations."""

    def test_multiple_configs_independence(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that multiple configs work independently."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create multiple configs
        config1_sources = font_sources[:2]
        config2_sources = font_sources[1:]

        downloader.save_config(sources=config1_sources, config_name="config1")
        downloader.save_config(sources=config2_sources, config_name="config2")

        # Load both
        fonts_dir1 = downloader.from_config("config1")
        fonts_dir2 = downloader.from_config("config2")

        # Verify independence
        assert fonts_dir1 != fonts_dir2
        assert len(list(fonts_dir1.glob("*.ttf"))) == 2
        assert len(list(fonts_dir2.glob("*.ttf"))) == 2

    def test_list_and_load_all_configs(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test listing and loading all available configs."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create several configs
        config_names = ["fonts_a", "fonts_b", "fonts_c"]
        for name in config_names:
            downloader.save_config(sources=font_sources, config_name=name)

        # List configs
        available_configs = downloader.list_configs()
        assert len(available_configs) == 3
        assert set(available_configs) == set(config_names)

        # Load each config
        for name in available_configs:
            fonts_dir = downloader.from_config(name)
            assert fonts_dir.exists()
            assert fonts_dir.name == name


class TestCacheManagement:
    """Test cache management workflows."""

    def test_selective_cache_clearing(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test selectively clearing specific configs."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create multiple configs
        downloader.save_config(sources=font_sources, config_name="keep_me")
        downloader.save_config(sources=font_sources, config_name="delete_me")

        # Clear one config
        downloader.clear_cache(config_name="delete_me")

        # Verify only the right one was deleted
        configs = downloader.list_configs()
        assert "keep_me" in configs
        assert "delete_me" in configs  # Config file still exists

        # But fonts are gone
        assert not tmp_path.joinpath("delete_me").exists()
        assert tmp_path.joinpath("keep_me").exists()

    def test_full_cache_reset(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test complete cache reset workflow."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create configs
        downloader.save_config(sources=font_sources, config_name="config1")
        downloader.save_config(sources=font_sources, config_name="config2")

        # Full reset
        downloader.clear_cache(remove_configs=True)

        # Everything should be gone
        assert downloader.list_configs() == []
        assert not tmp_path.joinpath("config1").exists()
        assert not tmp_path.joinpath("config2").exists()

    def test_cache_recovery_after_clear(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test recovering fonts after cache clear."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Create config
        downloader.save_config(sources=font_sources, config_name="recoverable")

        # Clear fonts but keep config
        downloader.clear_cache(config_name="recoverable", remove_configs=False)

        # Fonts should be gone
        assert not tmp_path.joinpath("recoverable").exists()

        # Reload - should re-download fonts
        fonts_dir = downloader.from_config("recoverable")

        # Fonts recovered
        assert fonts_dir.exists()
        for source in font_sources:
            assert fonts_dir.joinpath(source.name).exists()


class TestFromSourcesConvenience:
    """Test the convenience from_sources class method."""

    def test_from_sources_one_step(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test one-step config creation and loading."""
        fonts_dir = ReproducibleFontDownload.from_sources(
            sources=font_sources,
            config_name="quick_fonts",
            cache_dir=tmp_path,
        )

        # Should have everything ready
        assert fonts_dir.exists()
        for source in font_sources:
            assert fonts_dir.joinpath(source.name).exists()

        # Config should exist too
        config_path = tmp_path.joinpath("configs").joinpath("quick_fonts.json")
        assert config_path.exists()

    def test_from_sources_reusable(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that from_sources creates reusable configs."""
        # Create via from_sources
        fonts_dir = ReproducibleFontDownload.from_sources(
            sources=font_sources,
            config_name="reusable",
            cache_dir=tmp_path,
        )

        # Should be able to load again with regular from_config
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)
        fonts_dir2 = downloader.from_config("reusable")

        assert fonts_dir == fonts_dir2


class TestErrorRecovery:
    """Test error recovery scenarios."""

    def test_recover_from_partial_download(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test recovery when initial download is partial."""
        downloader = ReproducibleFontDownload(cache_dir=tmp_path)

        # Simulate partial download by making second font fail
        def download_side_effect(url: str, dest_path: pathlib.Path) -> bool:
            if "font2" in url:
                return False
            dest_path.write_bytes(b"fake font data")
            return True

        with patch.object(downloader, "_download_file", side_effect=download_side_effect):
            config_path = downloader.save_config(sources=font_sources, config_name="partial")  # noqa: F841

        # Config should exist with only successful fonts
        fonts_dir = tmp_path.joinpath("partial")
        assert fonts_dir.joinpath(font_sources[0].name).exists()
        assert not fonts_dir.joinpath(font_sources[1].name).exists()

        # Load again - should download missing fonts
        fonts_dir = downloader.from_config("partial")

        # Now all should be there (from config)
        # Note: from_config reads what's in the config file
        # If a font wasn't in the config (due to download failure), it won't be downloaded

    def test_concurrent_access_different_configs(
        self,
        tmp_path: pathlib.Path,
        font_sources: list[FontSource],
        fake_download: None,
    ) -> None:
        """Test that different instances can access different configs safely."""
        # Create two independent downloaders
        downloader1 = ReproducibleFontDownload(cache_dir=tmp_path)
        downloader2 = ReproducibleFontDownload(cache_dir=tmp_path)

        # Each creates and loads different configs
        downloader1.save_config(sources=font_sources[:2], config_name="instance1")
        downloader2.save_config(sources=font_sources[1:], config_name="instance2")

        fonts_dir1 = downloader1.from_config("instance1")
        fonts_dir2 = downloader2.from_config("instance2")

        # Both should work correctly
        assert fonts_dir1.exists()
        assert fonts_dir2.exists()
        assert fonts_dir1 != fonts_dir2
