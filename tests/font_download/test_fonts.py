"""Tests for font_download.fonts module."""

import hashlib
import pathlib

import pytest

from font_download.fonts import FontSource, FontEntity, combine_fonts, compute_file_sha256


class TestComputeFileSha256:
    """Test compute_file_sha256 function."""

    def test_computes_correct_hash(self, tmp_path):
        """Test SHA256 is computed correctly."""
        test_file = tmp_path / "test.ttf"
        content = b"test font content"
        test_file.write_bytes(content)

        result = compute_file_sha256(test_file)

        expected = hashlib.sha256(content).hexdigest()
        assert result == expected
        assert len(result) == 64  # SHA256 hex length

    def test_works_with_string_path(self, tmp_path):
        """Test function accepts string paths."""
        test_file = tmp_path / "test.ttf"
        test_file.write_bytes(b"content")

        result = compute_file_sha256(str(test_file))

        assert len(result) == 64


class TestFontSource:
    """Test FontSource dataclass."""

    def test_extracts_name_from_url(self):
        """Test that name is extracted from URL."""
        source = FontSource(url="https://example.com/fonts/Roboto-Regular.ttf")

        assert source.name == "Roboto-Regular.ttf"

    def test_handles_url_encoded_characters(self):
        """Test URL decoding."""
        source = FontSource(url="https://example.com/My%20Font.ttf")

        assert source.name == "My Font.ttf"

    def test_ignores_query_parameters(self):
        """Test that query params are ignored."""
        source = FontSource(url="https://example.com/font.ttf?version=1.0")

        assert source.name == "font.ttf"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        source = FontSource(url="https://example.com/font.ttf")

        result = source.to_dict()

        assert result == {"url": "https://example.com/font.ttf", "name": "font.ttf"}


class TestFontEntity:
    """Test FontEntity dataclass."""

    def test_creates_entity_with_hash(self, tmp_path):
        """Test FontEntity creation computes SHA256."""
        font_file = tmp_path / "font.ttf"
        content = b"font data"
        font_file.write_bytes(content)

        entity = FontEntity(
            name="font.ttf", url="https://example.com/font.ttf", file_path=font_file
        )

        assert entity.name == "font.ttf"
        assert entity.url == "https://example.com/font.ttf"
        assert entity.file_path == font_file
        assert entity.sha256 == hashlib.sha256(content).hexdigest()

    def test_converts_string_path_to_path(self, tmp_path):
        """Test string paths are converted to Path objects."""
        font_file = tmp_path / "font.ttf"
        font_file.write_bytes(b"content")

        entity = FontEntity(
            name="font.ttf", url="https://example.com/font.ttf", file_path=str(font_file)
        )

        assert isinstance(entity.file_path, pathlib.Path)

    def test_to_dict(self, tmp_path):
        """Test conversion to dictionary."""
        font_file = tmp_path / "font.ttf"
        font_file.write_bytes(b"content")

        entity = FontEntity(
            name="font.ttf", url="https://example.com/font.ttf", file_path=font_file
        )

        result = entity.to_dict()

        assert result["name"] == "font.ttf"
        assert result["url"] == "https://example.com/font.ttf"
        assert "sha256" in result
        assert len(result["sha256"]) == 64


class TestCombineFonts:
    """Test combine_fonts function."""

    def test_combines_multiple_lists(self):
        """Test combining multiple font lists."""
        list1 = [FontSource(url="https://example.com/a.ttf")]
        list2 = [FontSource(url="https://example.com/b.ttf")]

        result = combine_fonts(list1, list2)

        assert len(result) == 2
        assert result[0].name == "a.ttf"
        assert result[1].name == "b.ttf"

    def test_detects_duplicate_urls(self):
        """Test that duplicate URLs raise an error."""
        list1 = [FontSource(url="https://example.com/font.ttf")]
        list2 = [FontSource(url="https://example.com/font.ttf")]

        with pytest.raises(ValueError, match="Duplicate URLs"):
            combine_fonts(list1, list2)

    def test_detects_duplicate_names(self):
        """Test that duplicate names raise an error."""
        list1 = [FontSource(url="https://example.com/fonts/a/font.ttf")]
        list2 = [FontSource(url="https://example.com/fonts/b/font.ttf")]

        with pytest.raises(ValueError, match="Duplicate names"):
            combine_fonts(list1, list2)

    def test_allows_unique_fonts(self):
        """Test that unique fonts are combined successfully."""
        list1 = [FontSource(url="https://example.com/font1.ttf")]
        list2 = [FontSource(url="https://example.com/font2.ttf")]
        list3 = [FontSource(url="https://example.com/font3.ttf")]

        result = combine_fonts(list1, list2, list3)

        assert len(result) == 3
