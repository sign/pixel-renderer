import logging
import pathlib
from dataclasses import dataclass

from font_configurator.font_configurator import FontConfigurator
from font_configurator.fontconfig_managers import FontconfigMode
from font_download.reproducible_font_download import ReproducibleFontDownload
from font_download.reproducible_fonts.honk import FONTS_HONK
from font_download.reproducible_fonts.noto_sans import FONTS_NOTO_SANS, FONTS_NOTO_SANS_BW
from font_download.tools import FontSource
from pixel_renderer.renderer import render_text_image

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")


@dataclass(slots=True)
class RenderExample:
    """Configuration for a text rendering example."""

    text: str
    image_name: str
    sources: list[FontSource]
    config_name: str
    block_size: int = 16
    font_size: int = 20


def demo_render_text_image(
    text: str,
    image_name: str,
    sources: list[FontSource],
    config_name: str,
    block_size: int = 16,
    font_size: int = 20,
) -> None:
    result_dir = pathlib.Path("demos_output/demo_renderer")
    result_dir.mkdir(parents=True, exist_ok=True)

    font_downloader = ReproducibleFontDownload()
    font_dir = font_downloader.from_sources(sources=sources, config_name=config_name)  # assuming first time use

    font_configurator = FontConfigurator()
    font_configurator.setup_font(
        mode=FontconfigMode.TEMPLATE_MINIMAL,
        font_dir=font_dir,
        fontconfig_destination_dir=f".cache/font_configurator/{image_name}_fontconfig",  # mimic unique dir per image
        force_reinitialize=True,
    )

    image = render_text_image(text=text, block_size=block_size, font_size=font_size)
    image_path = result_dir.joinpath(image_name).with_suffix(".png")
    image.save(image_path)
    print(f"Rendered '{text}' and saved as '{image_name}'")
    print(f"Image size: {image.size}")


if __name__ == "__main__":
    examples = [
        RenderExample(
            text="hello🤗\r\n\x02 ",
            image_name="hello_example",
            sources=FONTS_NOTO_SANS,
            config_name="noto_sans",
            block_size=16,
            font_size=20,
        ),
        RenderExample(
            text="black and white emojis 🤗👹",
            image_name="bw_emoji_example",
            sources=FONTS_NOTO_SANS_BW,
            config_name="noto_sans_bw",
            block_size=16,
            font_size=20,
        ),
        RenderExample(
            text="Using Honk font! 🤡🎉",  # expected to have not rendered emojis because of FontconfigMode.TEMPLATE_MINIMAL  # noqa: E501
            image_name="honk_font_example",
            sources=FONTS_HONK,
            config_name="honk_only",
            block_size=16,
            font_size=20,
        ),
    ]
    for example in examples:
        demo_render_text_image(
            text=example.text,
            image_name=example.image_name,
            sources=example.sources,
            config_name=example.config_name,
            block_size=example.block_size,
            font_size=example.font_size,
        )
