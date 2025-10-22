"""Shared fixtures for font_download tests."""

import pathlib
import tempfile
from unittest.mock import Mock, patch

import pytest

from font_download.fonts import FontSource


@pytest.fixture
def font_sources():
    """Sample font sources for testing."""
    return [
        FontSource(url="https://example.com/fonts/font1.ttf"),
        FontSource(url="https://example.com/fonts/font2.ttf"),
    ]


@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create a temporary cache directory."""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def mock_download_setup(temp_cache_dir):
    """Mock urlretrieve and set temporary cache directory."""

    def fake_urlretrieve(url, filename):
        # Create fake font file with unique content based on URL
        pathlib.Path(filename).write_bytes(f"font-content-{url}".encode())

    with patch("font_download.download_fonts.urlretrieve", fake_urlretrieve), \
         patch("font_download.download_fonts.FONT_DOWNLOAD_CACHE_DIR", temp_cache_dir):
        yield temp_cache_dir


@pytest.fixture
def mock_processor_setup(mock_download_setup):
    """Mock both download and FontConfigurator for processor tests."""
    # Mock FontConfigurator - it's not imported in processor.py anymore based on user's changes
    # So we don't need to mock it
    yield mock_download_setup
