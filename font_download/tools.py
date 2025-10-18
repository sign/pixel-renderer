# Copyright 2025- Pavel Stepachev
# SPDX-License-Identifier: Apache-2.0
import hashlib
import pathlib
from dataclasses import asdict, dataclass
from urllib.parse import unquote, urlparse


class ReproducibleFontDownloadUtils:
    @staticmethod
    def compute_sha256(file_path: str | pathlib.Path) -> str:
        if not isinstance(file_path, pathlib.Path):
            file_path = pathlib.Path(file_path)

        if not file_path.is_file():
            msg = f"File {file_path} does not exist or is not a file."
            raise FileNotFoundError(msg)

        hash_sha256 = hashlib.sha256()
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)

        return hash_sha256.hexdigest()


@dataclass(slots=True)
class FontSource:
    """Represents a font to be downloaded, as provided by the user."""

    url: str
    name: str = "placeholder_name"

    def __post_init__(self):
        self.prepare_name()

    def prepare_name(self) -> str:
        parsed_url = urlparse(self.url)
        self.name = pathlib.Path(unquote(parsed_url.path)).name
        return self.name

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class FontEntity:
    """Represents a font's metadata in the JSON configuration file."""

    name: str
    url: str

    file_path: pathlib.Path
    sha256: str = ""

    def __post_init__(self):
        if not isinstance(self.file_path, pathlib.Path):
            self.file_path = pathlib.Path(self.file_path)

        self.sha256 = ReproducibleFontDownloadUtils.compute_sha256(file_path=self.file_path)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_config_format_dict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "sha256": self.sha256,
        }
