


# How to use

## Scenario 1: Create config then load
```python
from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.tools import FontSource

list_font_sources = [
    FontSource(
        url="here_goes_font_url",
    ),
]


downloader = ReproducibleFontDownload()

# save config
config_path = downloader.save_config(sources=list_font_sources, config_name="my_fonts")

# load fonts
fonts_dir = downloader.from_config(config_name_or_path="my_fonts")
```

## Scenario 2: Load existing config

```python
from font_download.reproducible_font_download import ReproducibleFontDownload

downloader = ReproducibleFontDownload()

# by name (looks in cache/configs/)
fonts_dir = downloader.from_config(config_name_or_path="my_fonts")

# by path
fonts_dir = downloader.from_config(config_name_or_path="/path/to/config.json")

# force re-download
fonts_dir = downloader.from_config(config_name_or_path="my_fonts", force_download=True)
```

## In single step 
```python
from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.tools import FontSource

list_font_sources = [
    FontSource(
        url="here_goes_font_url",
    ),
]


fonts_dir = ReproducibleFontDownload.from_sources(sources=list_font_sources, config_name="my_fonts")
```

