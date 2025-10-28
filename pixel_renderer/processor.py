from __future__ import annotations

from transformers import AutoVideoProcessor, ProcessorMixin

from font_configurator.font_configurator import FontConfigurator
from font_configurator.fontconfig_managers import FontconfigMode
from font_download import FontConfig
from pixel_renderer.renderer import render_text, render_text_image


class PixelRendererProcessor(ProcessorMixin):
    name = "pixel-renderer-processor"
    attributes = []

    def __init__(self,
                 font: FontConfig = None,
                 **kwargs) -> None:
        super().__init__(**kwargs)

        if isinstance(font, dict):
            font = FontConfig.from_dict(font)
        self.font = font

        if self.font is not None:
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
        if self.font is None:
            raise ValueError("FontConfig must be provided to render text.")
        # It might not be obvious why we repeat the `render_text` function here instead of using
        # the one from `pixel_renderer.renderer`. The reason is that we want to ensure that
        # the fontconfig is properly set up before rendering the text. By having this method
        # in the processor, we can guarantee that the fontconfig setup is done when the processor
        # is initialized. and in the future, that nothing has overwritten the fontconfig setup.
        return render_text(text, block_size=block_size, font_size=font_size)

    def render_text_image(self, text: str, block_size: int = 16, font_size: int = 12):
        return render_text_image(text, block_size=block_size, font_size=font_size)

    def to_dict(self, **unused_kwargs):
        return {
            "font": self.font.to_dict(),
        }


# TODO: register to AutoProcessor instead
#  Using video processor as a workaround https://github.com/huggingface/transformers/issues/41816
AutoVideoProcessor.register(FontConfig, PixelRendererProcessor)
