from font_download.tools import FontSource, _check_no_duplicates

_HONK = [
    FontSource(
        # ofl/honk/Honk[MORF,SHLN].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/honk/Honk%5BMORF,SHLN%5D.ttf",
    ),
]

FONTS_HONK = _check_no_duplicates(
    _HONK,
)
