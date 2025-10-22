from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS
from pixel_renderer import PixelRendererProcessor

if __name__ == "__main__":
    font_config = FontConfig(sources=FONTS_NOTO_SANS)
    pixel_processor = PixelRendererProcessor(font=font_config)

    pixel_processor.render_text_image("hello!").save("demos_output/hello.png")

    pixel_processor.save_pretrained("demos_output/processor")
