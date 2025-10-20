# How to use

This tool provides reproducible font downloads with integrity verification. You can either create new font configurations or use existing ones.

## Scenario 1: Create and use a new configuration

Create your own list of fonts using `FontSource` objects or use prepared collections:

```python
from font_download.reproducible_fonts.honk import FONTS_HONK
from font_download.reproducible_fonts.noto_sans import (
    FONTS_NOTO_SANS, 
    FONTS_NOTO_SANS_BW, 
    FONTS_NOTO_SANS_MINIMAL
)
```

### Step 1: Create configuration and download fonts

```python
from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.tools import FontSource

list_font_sources = [
    FontSource(
        url="https://github.com/google/fonts/raw/.../NotoSans.ttf",
    ),
]

downloader = ReproducibleFontDownload()

# Downloads fonts and saves configuration with SHA256 hashes
config_path = downloader.save_config(sources=list_font_sources, config_name="my_fonts")
```

This creates a JSON configuration file like:

```json
[
    {
        "name": "NotoSansDevanagari[wdth,wght].ttf",
        "url": "https://github.com/google/fonts/raw/601944d2ee97e76d4c456dc3d790db358c0c6ec5/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth,wght%5D.ttf",
        "sha256": "9ce7b04f60e363d8870e5997744cf85cf69d38a4d7d129d364d92a3b14b461d7"
    }
]
```

### Step 2: Load fonts from configuration

```python
# Loads fonts, verifies integrity, downloads missing fonts if needed
fonts_dir = downloader.from_config(config_name_or_path="my_fonts")

# fonts_dir can now be used with font_configurator
```

**Key benefit**: Automatically generates download configurations with integrity hashes instead of manually creating JSON files. This ensures reproducible font downloads across different environments.

## Scenario 2: Use existing configuration

If you already have a configuration file, simply load it:

```python
from font_download.reproducible_font_download import ReproducibleFontDownload

downloader = ReproducibleFontDownload()

# Load by config name (looks in .cache/pixel_renderer/fonts/configs/)
fonts_dir = downloader.from_config(config_name_or_path="my_fonts")

# Or load by absolute path
fonts_dir = downloader.from_config(config_name_or_path="/path/to/config.json")

# Force re-download all fonts (even if cached)
fonts_dir = downloader.from_config(config_name_or_path="my_fonts", force_download=True)
```

## Scenario 3: One-step download (convenience method)

Combines configuration creation and font loading in a single call:

```python
from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.tools import FontSource

list_font_sources = [
    FontSource(
        url="https://github.com/google/fonts/raw/.../NotoSans.ttf",
    ),
]

# Creates config and returns fonts directory in one step
fonts_dir = ReproducibleFontDownload.from_sources(
    sources=list_font_sources, 
    config_name="my_fonts"
)
```

## Additional operations

```python
downloader = ReproducibleFontDownload()

# List all available configurations
configs = downloader.list_configs()

# Clear cached fonts for specific config
downloader.clear_cache("my_fonts")

# Clear all cached fonts
downloader.clear_cache()

# Clear everything including config files
downloader.clear_cache(remove_configs=True)
```