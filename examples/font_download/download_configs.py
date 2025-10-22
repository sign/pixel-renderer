import logging

from font_download import download_fonts
from font_download.example_fonts.honk import FONTS_HONK
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS, FONTS_NOTO_SANS_BW, FONTS_NOTO_SANS_MINIMAL

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

if __name__ == "__main__":
    mapping = {
        "noto_sans": FONTS_NOTO_SANS,
        "noto_sans_bw": FONTS_NOTO_SANS_BW,
        "noto_sans_minimal": FONTS_NOTO_SANS_MINIMAL,
        "honk_only": FONTS_HONK,
    }

    for config_name, sources in mapping.items():
        fonts_dir = download_fonts(sources=sources)
        print(f"Created font download config '{config_name}':")
        print(f"  Fonts dir: {fonts_dir}")
