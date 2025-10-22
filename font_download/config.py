from transformers import AutoConfig, PretrainedConfig

from font_download.download_fonts import download_fonts
from font_download.fonts import FontSource, FontsSources


class FontConfig(PretrainedConfig):
    model_type = "font_config"

    def __init__(self, sources: FontsSources | None = None, **kwargs) -> None:
        super().__init__(**kwargs)

        if isinstance(sources, list) and any(not isinstance(s, dict) for s in sources):
            sources = [s.to_dict() for s in sources]

        self.sources = sources

    def get_font_dir(self):
        sources = self.sources
        # Convert list of dicts to list of FontSource objects if needed
        if isinstance(sources, list) and all(isinstance(s, dict) for s in sources):
            sources = [FontSource(url=s["url"], name=s["name"]) for s in sources]
        return download_fonts(sources)


AutoConfig.register(FontConfig.model_type, FontConfig)
FontConfig.register_for_auto_class(AutoConfig)
