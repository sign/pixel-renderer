import pathlib
from unittest.mock import Mock

import pytest

from font_download.tools import FontEntity, FontSource, ReproducibleFontDownloadUtils


@pytest.fixture
def font_sources() -> list[FontSource]:
    """Return a list of FontSource objects with dummy URLs."""
    return [
        FontSource(url="https://example.com/fonts/font1.ttf"),
        FontSource(url="https://example.com/fonts/font2.ttf"),
        FontSource(url="https://example.com/fonts/font3.ttf"),
    ]


@pytest.fixture
def fake_download(monkeypatch: pytest.MonkeyPatch, mock_fonts: list[FontEntity]) -> None:
    """Mock requests.get to simulate font downloads."""

    def mock_get(url: str, stream: bool = False, timeout: int = 30):  # noqa: ARG001
        mock_response = Mock()

        # Create a proper headers mock that returns strings
        headers_mock = Mock()
        headers_mock.get = Mock(return_value="1024")
        mock_response.headers = headers_mock

        # Simulate font content based on URL
        for font in mock_fonts:
            if font.url == url:
                content = f"mock-font-content-{font.name}".encode()
                mock_response.iter_content.return_value = [content]
                break
        else:
            mock_response.iter_content.return_value = [b"default-content"]

        mock_response.raise_for_status = Mock()
        mock_response.__enter__ = Mock(return_value=mock_response)
        mock_response.__exit__ = Mock(return_value=False)

        return mock_response

    monkeypatch.setattr("requests.get", mock_get)


@pytest.fixture
def mock_fonts(tmp_path: pathlib.Path, font_sources: list[FontSource]) -> list[FontEntity]:
    """Create temporary files and corresponding FontEntity objects."""
    mock_fonts: list[FontEntity] = []
    for source in font_sources:
        file_path = tmp_path.joinpath(source.name)
        content = f"mock-font-content-{source.name}".encode()
        file_path.write_bytes(content)
        sha256 = ReproducibleFontDownloadUtils.compute_sha256(file_path)
        mock_fonts.append(FontEntity(name=source.name, url=source.url, file_path=file_path, sha256=sha256))
    return mock_fonts
