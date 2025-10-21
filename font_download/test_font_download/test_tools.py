"""Tests for font_download.tools module."""

import hashlib
import pathlib

import pytest

from font_download.tools import (
    FontEntity,
    FontSource,
    ReproducibleFontDownloadUtils,
)


class TestReproducibleFontDownloadUtils:
    """Test utility functions."""

    def test_compute_sha256_valid_file(self, tmp_path: pathlib.Path) -> None:
        """Test SHA256 computation for valid file."""
        test_file = tmp_path / "test.txt"
        test_content = b"Hello, World!" * 1000
        test_file.write_bytes(test_content)

        result = ReproducibleFontDownloadUtils.compute_sha256(test_file)

        # verify against known hash
        expected = hashlib.sha256(test_content).hexdigest()
        assert result == expected
        assert len(result) == 64  # SHA256 produces 64 hex characters  # noqa: PLR2004

    def test_compute_sha256_with_string_path(self, tmp_path: pathlib.Path) -> None:
        """Test SHA256 computation with string path."""
        test_file = tmp_path / "test.txt"
        test_content = b"Test content"
        test_file.write_bytes(test_content)

        result = ReproducibleFontDownloadUtils.compute_sha256(str(test_file))

        expected = hashlib.sha256(test_content).hexdigest()
        assert result == expected

    def test_compute_sha256_missing_file(self, tmp_path: pathlib.Path) -> None:
        """Test SHA256 computation for missing file raises error."""
        missing_file = tmp_path / "nonexistent.txt"

        with pytest.raises(FileNotFoundError, match="does not exist"):
            ReproducibleFontDownloadUtils.compute_sha256(missing_file)

    def test_compute_sha256_directory_raises_error(self, tmp_path: pathlib.Path) -> None:
        """Test SHA256 computation for directory raises error."""
        with pytest.raises(FileNotFoundError, match="not a file"):
            ReproducibleFontDownloadUtils.compute_sha256(tmp_path)

    def test_compute_sha256_empty_file(self, tmp_path: pathlib.Path) -> None:
        """Test SHA256 computation for empty file."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_bytes(b"")

        result = ReproducibleFontDownloadUtils.compute_sha256(empty_file)

        # SHA256 of empty file
        expected = hashlib.sha256(b"").hexdigest()
        assert result == expected

    def test_compute_sha256_large_file(self, tmp_path: pathlib.Path) -> None:
        """Test SHA256 computation for large file (tests chunked reading)."""
        large_file = tmp_path / "large.bin"
        # create a file larger than 4096 bytes (chunk size)
        large_content = b"X" * 10000
        large_file.write_bytes(large_content)

        result = ReproducibleFontDownloadUtils.compute_sha256(large_file)

        expected = hashlib.sha256(large_content).hexdigest()
        assert result == expected


class TestFontSource:
    """Test FontSource dataclass."""

    def test_font_source_basic_creation(self) -> None:
        """Test basic FontSource creation."""
        source = FontSource(url="https://example.com/font.ttf")

        assert source.url == "https://example.com/font.ttf"
        assert source.name == "font.ttf"

    def test_font_source_with_explicit_name(self) -> None:
        """Test FontSource with explicitly provided name."""
        source = FontSource(url="https://example.com/font.ttf", name="custom_name.ttf")

        # name should be overridden by prepare_name in __post_init__
        assert source.name == "font.ttf"

    def test_font_source_prepare_name_from_url(self) -> None:
        """Test automatic name extraction from URL."""
        source = FontSource(url="https://example.com/path/to/Roboto-Regular.ttf")

        assert source.name == "Roboto-Regular.ttf"

    def test_font_source_prepare_name_url_encoded(self) -> None:
        """Test name extraction with URL-encoded characters."""
        source = FontSource(url="https://example.com/My%20Font%20Name.ttf")

        assert source.name == "My Font Name.ttf"

    def test_font_source_prepare_name_complex_url(self) -> None:
        """Test name extraction from complex URL with query parameters."""
        source = FontSource(url="https://example.com/fonts/Arial.ttf?version=1.0&format=truetype")

        # should extract just the filename, ignoring query params
        assert source.name == "Arial.ttf"

    def test_font_source_to_dict(self) -> None:
        """Test conversion to dictionary."""
        source = FontSource(url="https://example.com/font.ttf")

        result = source.to_dict()

        assert isinstance(result, dict)
        assert result["url"] == "https://example.com/font.ttf"
        assert result["name"] == "font.ttf"

    def test_font_source_slots(self) -> None:
        """Test that FontSource uses slots."""
        source = FontSource(url="https://example.com/font.ttf")

        # slots prevent adding arbitrary attributes
        with pytest.raises(AttributeError):
            source.arbitrary_attribute = "value"  # type: ignore[attr-defined]


class TestFontEntity:
    """Test FontEntity dataclass."""

    def test_font_entity_creation(self, tmp_path: pathlib.Path) -> None:
        """Test basic FontEntity creation."""
        test_file = tmp_path / "test_font.ttf"
        test_content = b"Mock font content"
        test_file.write_bytes(test_content)

        entity = FontEntity(
            name="test_font.ttf",
            url="https://example.com/test_font.ttf",
            file_path=test_file,
        )

        assert entity.name == "test_font.ttf"
        assert entity.url == "https://example.com/test_font.ttf"
        assert entity.file_path == test_file
        assert entity.sha256 == hashlib.sha256(test_content).hexdigest()

    def test_font_entity_auto_computes_sha256(self, tmp_path: pathlib.Path) -> None:
        """Test that SHA256 is automatically computed in __post_init__."""
        test_file = tmp_path / "font.ttf"
        test_content = b"Font data for hashing"
        test_file.write_bytes(test_content)

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
        )

        expected_hash = hashlib.sha256(test_content).hexdigest()
        assert entity.sha256 == expected_hash

    def test_font_entity_string_path_converted(self, tmp_path: pathlib.Path) -> None:
        """Test that string paths are converted to pathlib.Path."""
        test_file = tmp_path / "font.ttf"
        test_file.write_bytes(b"content")

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=str(test_file),  # type: ignore[arg-type] # pass as string
        )

        assert isinstance(entity.file_path, pathlib.Path)
        assert entity.file_path == test_file

    def test_font_entity_to_dict(self, tmp_path: pathlib.Path) -> None:
        """Test conversion to dictionary."""
        test_file = tmp_path / "font.ttf"
        test_file.write_bytes(b"content")

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
        )

        result = entity.to_dict()

        assert isinstance(result, dict)
        assert result["name"] == "font.ttf"
        assert result["url"] == "https://example.com/font.ttf"
        assert result["file_path"] == test_file
        assert "sha256" in result

    def test_font_entity_to_config_format_dict(self, tmp_path: pathlib.Path) -> None:
        """Test conversion to config format (excludes file_path)."""
        test_file = tmp_path / "font.ttf"
        test_content = b"content"
        test_file.write_bytes(test_content)

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
        )

        result = entity.to_config_format_dict()

        assert isinstance(result, dict)
        assert result["name"] == "font.ttf"
        assert result["url"] == "https://example.com/font.ttf"
        assert result["sha256"] == hashlib.sha256(test_content).hexdigest()
        assert "file_path" not in result  # should not include file_path in config

    def test_font_entity_missing_file_raises_error(self, tmp_path: pathlib.Path) -> None:
        """Test that missing file raises error during creation."""
        missing_file = tmp_path / "nonexistent.ttf"

        with pytest.raises(FileNotFoundError):
            FontEntity(
                name="nonexistent.ttf",
                url="https://example.com/nonexistent.ttf",
                file_path=missing_file,
            )

    def test_font_entity_sha256_override_ignored(self, tmp_path: pathlib.Path) -> None:
        """Test that manually provided SHA256 is overridden by computed value."""
        test_file = tmp_path / "font.ttf"
        test_content = b"content"
        test_file.write_bytes(test_content)

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
            sha256="wrong_hash",  # this should be overridden
        )

        # should compute correct hash, not use the provided one
        expected_hash = hashlib.sha256(test_content).hexdigest()
        assert entity.sha256 == expected_hash
        assert entity.sha256 != "wrong_hash"

    def test_font_entity_slots(self, tmp_path: pathlib.Path) -> None:
        """Test that FontEntity uses slots."""
        test_file = tmp_path / "font.ttf"
        test_file.write_bytes(b"content")

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
        )

        # slots prevent adding arbitrary attributes
        with pytest.raises(AttributeError):
            entity.arbitrary_attribute = "value"  # type: ignore[attr-defined]


class TestFontSourceAndEntityIntegration:
    """Test integration between FontSource and FontEntity."""

    def test_source_to_entity_workflow(self, tmp_path: pathlib.Path) -> None:
        """Test workflow from FontSource to FontEntity."""
        # create a source
        source = FontSource(url="https://example.com/fonts/MyFont.ttf")

        # simulate downloading the font
        font_file = tmp_path / source.name
        font_content = b"Downloaded font content"
        font_file.write_bytes(font_content)

        # create entity from downloaded file
        entity = FontEntity(
            name=source.name,
            url=source.url,
            file_path=font_file,
        )

        assert entity.name == source.name
        assert entity.url == source.url
        assert entity.file_path == font_file
        assert entity.sha256 == hashlib.sha256(font_content).hexdigest()

    def test_multiple_sources_to_entities(self, tmp_path: pathlib.Path) -> None:
        """Test processing multiple sources into entities."""
        sources = [
            FontSource(url="https://example.com/font1.ttf"),
            FontSource(url="https://example.com/font2.ttf"),
            FontSource(url="https://example.com/font3.ttf"),
        ]

        entities = []
        for source in sources:
            font_file = tmp_path / source.name
            font_file.write_bytes(f"Content for {source.name}".encode())

            entity = FontEntity(
                name=source.name,
                url=source.url,
                file_path=font_file,
            )
            entities.append(entity)

        assert len(entities) == 3  # noqa: PLR2004
        for i, entity in enumerate(entities):
            assert entity.name == sources[i].name
            assert entity.url == sources[i].url
            assert entity.sha256  # should have computed hash

    def test_entity_config_format_matches_json_structure(self, tmp_path: pathlib.Path) -> None:
        """Test that entity config format matches expected JSON structure."""
        test_file = tmp_path / "font.ttf"
        test_file.write_bytes(b"content")

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
        )

        config_dict = entity.to_config_format_dict()

        # verify it has exactly the fields we expect in config files
        assert set(config_dict.keys()) == {"name", "url", "sha256"}
        assert all(isinstance(v, str) for v in config_dict.values())


class TestEdgeCasesTools:
    """Test edge cases in tools module."""

    def test_font_source_empty_url(self) -> None:
        """Test FontSource with empty URL."""
        source = FontSource(url="")
        assert source.name == ""

    def test_font_source_url_with_fragment(self) -> None:
        """Test URL with fragment identifier."""
        source = FontSource(url="https://example.com/font.ttf#section")
        assert source.name == "font.ttf"

    def test_font_source_url_trailing_slash(self) -> None:
        """Test URL with trailing slash."""
        source = FontSource(url="https://example.com/fonts/")
        # pathlib extracts the directory name when URL ends with /
        assert source.name == "fonts"

    def test_font_entity_with_unicode_content(self, tmp_path: pathlib.Path) -> None:
        """Test FontEntity with unicode characters in content."""
        test_file = tmp_path / "font.ttf"
        unicode_content = "Unicode: café, 日本語, émojis 🎉".encode("utf-8")  # noqa: UP012
        test_file.write_bytes(unicode_content)

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
        )

        expected_hash = hashlib.sha256(unicode_content).hexdigest()
        assert entity.sha256 == expected_hash

    def test_font_entity_binary_content(self, tmp_path: pathlib.Path) -> None:
        """Test FontEntity with actual binary font-like content."""
        test_file = tmp_path / "font.ttf"
        # simulate binary font data
        binary_content = bytes(range(256)) * 100
        test_file.write_bytes(binary_content)

        entity = FontEntity(
            name="font.ttf",
            url="https://example.com/font.ttf",
            file_path=test_file,
        )

        assert entity.sha256
        assert len(entity.sha256) == 64  # noqa: PLR2004
