import hashlib
import pathlib
from collections import defaultdict
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

    def __post_init__(self) -> None:
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

    def __post_init__(self) -> None:
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


def _check_no_duplicates(*font_lists: list[FontSource]) -> list[FontSource]:
    """Validate that there are no duplicate fonts by URL or name.

    Args:
        *font_lists: Variable number of font source lists to check

    Returns:
        Combined list of all FontSource objects if no duplicates found

    Raises:
        ValueError: If duplicate URLs or names are found
    """
    all_fonts = []
    for font_list in font_lists:
        all_fonts.extend(font_list)

    url_map = defaultdict(list)
    name_map = defaultdict(list)

    for idx, font in enumerate(all_fonts):
        url_map[font.url].append(idx)
        name_map[font.name].append(idx)

    # check for duplicates
    duplicate_urls = {url: indices for url, indices in url_map.items() if len(indices) > 1}
    duplicate_names = {name: indices for name, indices in name_map.items() if len(indices) > 1}

    errors = []

    if duplicate_urls:
        errors.append("Duplicate URLs found:")
        for url, indices in duplicate_urls.items():
            errors.append(f"  URL: {url}")
            errors.append(f"    Found at indices: {indices}")

    if duplicate_names:
        if errors:
            errors.append("")
        errors.append("Duplicate names found:")
        for name, indices in duplicate_names.items():
            errors.append(f"  Name: {name}")
            errors.append(f"    Found at indices: {indices}")
            for idx in indices:
                errors.append(f"      [{idx}] {all_fonts[idx].url}")

    if errors:
        raise ValueError("\n".join(errors))

    return all_fonts
