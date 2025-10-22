import hashlib
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


def compute_file_sha256(file_path: str | Path) -> str:
    with open(file_path, 'rb', buffering=0) as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

@dataclass(slots=True)
class FontSource:
    """Represents a font to be downloaded, as provided by the user."""

    url: str
    name: str = "placeholder_name"

    def __post_init__(self) -> None:
        self.prepare_name()

    def prepare_name(self) -> str:
        parsed_url = urlparse(self.url)
        self.name = Path(unquote(parsed_url.path)).name
        return self.name

    def to_dict(self) -> dict:
        return asdict(self)

FontSourceDict = dict[str, str]

FontsSources = list[FontSource] | list[FontSourceDict]

@dataclass(slots=True)
class FontEntity:
    """Represents a font's metadata in the JSON configuration file."""

    name: str
    url: str
    file_path: Path

    sha256: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.file_path, Path):
            self.file_path = Path(self.file_path)

        self.sha256 = compute_file_sha256(file_path=self.file_path)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "url": self.url,
            "sha256": self.sha256,
        }


def combine_fonts(*font_lists: FontsSources) -> FontsSources:
    """Combine fount sources, while validating that there are no duplicate fonts by URL or name.

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
