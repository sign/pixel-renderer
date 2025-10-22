from __future__ import annotations

from typing import Any

from transformers import ProcessorMixin

from font_configurator.font_configurator import FontConfigurator
from font_configurator.fontconfig_managers import FontconfigMode
from font_download import FontConfig, FontConfig
from pixel_renderer.renderer import render_text_image, render_text


class PixelRendererProcessor(ProcessorMixin):
    name = "pixel-renderer-processor"
    attributes = []

    def __init__(self,
                 font: FontConfig,
                 **kwargs) -> None:
        super().__init__(**kwargs)

        if isinstance(font, dict):
            font = FontConfig.from_dict(font)
        self.font = font

        font_dir = font.get_font_dir()

        # Configure fontconfig (minimal template)
        font_configurator = FontConfigurator()
        self.fontconfig_path = font_configurator.setup_font(
            mode=FontconfigMode.TEMPLATE_MINIMAL,
            font_dir=font_dir,
            fontconfig_destination_dir=font_dir,
            force_reinitialize=True,
        )

    def render_text(self, text: str, block_size: int = 16, font_size: int = 12):
        return render_text(text, block_size=block_size, font_size=font_size)

    def render_text_image(self, text: str, block_size: int = 16, font_size: int = 12):
        return render_text_image(text, block_size=block_size, font_size=font_size)

    def to_dict(self, **unused_kwargs):
        return {
            "font": self.font.to_dict(),
        }