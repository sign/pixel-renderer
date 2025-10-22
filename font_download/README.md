# How to use

This tool provides reproducible font downloads with integrity verification. You can either create new font
configurations or use existing ones.

## Create and use a new configuration

Create your own list of fonts using `FontSource` objects or use prepared collections:

```python
from font_download.example_fonts.honk import FONTS_HONK
from font_download.example_fonts.noto_sans import (
    FONTS_NOTO_SANS,
    FONTS_NOTO_SANS_BW,
    FONTS_NOTO_SANS_MINIMAL
)
```

### Step 1: Create configuration and download fonts

```python
from font_download import download_fonts
from font_download.fonts import FontSource

font_sources = [
    FontSource(url="https://github.com/google/fonts/raw/.../NotoSans.ttf"),
]

# Downloads fonts and saves configuration with SHA256 hashes
fonts_dir = download_fonts(font_sources)
```

This creates a directory with the fonts, and a JSON configuration file like:

```json
[
  {
    "name": "NotoSansDevanagari[wdth,wght].ttf",
    "url": "https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth,wght%5D.ttf",
    "sha256": "9ce7b04f60e363d8870e5997744cf85cf69d38a4d7d129d364d92a3b14b461d7"
  }
]
```

### Step 2: Save and load configurations

```python
from font_download import FontConfig

processor = FontConfig(sources=font_sources)
processor.save_pretrained("example")

# Later, load fonts using the saved configuration
fonts_dir = processor.from_pretrained("example")
```
