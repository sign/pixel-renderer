from font_download.fonts import FontSource, combine_fonts

_HONK = [
    FontSource(
        # ofl/honk/Honk[MORF,SHLN].ttf
        url="https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/honk/Honk%5BMORF,SHLN%5D.ttf",
    ),
]

FONTS_HONK = combine_fonts(
    _HONK,
)
