import logging
import pathlib

from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.reproducible_fonts.honk import FONTS_HONK
from font_download.reproducible_fonts.noto_sans import FONTS_NOTO_SANS, FONTS_NOTO_SANS_BW, FONTS_NOTO_SANS_MINIMAL
from font_download.tools import FontSource

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


def create_font_download_configs(
    sources: list[FontSource], config_name: str, dest_dir: str | pathlib.Path | None = None
) -> tuple[pathlib.Path, pathlib.Path]:
    reproduce = ReproducibleFontDownload()

    fonts_dir = reproduce.from_sources(sources=sources, config_name=config_name, cache_dir=dest_dir)

    download_font_config = reproduce.resolve_config_path(config_name_or_path=config_name)

    return fonts_dir, download_font_config


if __name__ == "__main__":
    mapping = {
        "noto_sans": FONTS_NOTO_SANS,
        "noto_sans_bw": FONTS_NOTO_SANS_BW,
        "noto_sans_minimal": FONTS_NOTO_SANS_MINIMAL,
        "honk_only": FONTS_HONK,
    }

    for config_name, sources in mapping.items():
        fonts_dir, config_path = create_font_download_configs(
            sources=sources, config_name=config_name, dest_dir="demos_output/create_font_download_configs"
        )
        print(f"Created font download config '{config_name}':")
        print(f"  Fonts dir: {fonts_dir}")
        print(f"  Config path: {config_path}")
