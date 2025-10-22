# PIXEL Renderer

This repository contains a text renderer for PIXEL models.

## Usage

Install dependencies:

```shell
conda create -n pixel python=3.12 -y
conda activate pixel
pip install ".[dev,pangocairo]"
```

> [!TIP]
> Having trouble installing `pycairo` and `pygobject`? 
> See [these instructions](https://pygobject.readthedocs.io/en/latest/getting_started.html#installing-pygobject).

Install:

```bash
pip install "pixel-renderer[pangocairo]"
```

Render text as an image (array):

```python
from pixel_renderer.renderer import render_text

render_text(text="test", block_size=16, font_size=12)
```

For better consistency across platforms and easier reproducibility, we need to specify the exact fonts.


```python
from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS
from pixel_renderer import PixelRendererProcessor

font_config = FontConfig(sources=FONTS_NOTO_SANS)
pixel_processor = PixelRendererProcessor(font=font_config)

pixel_processor.render_text_image("hello!").save("demos_output/hello.png")

pixel_processor.save_pretrained("demos_output/processor")
```

## Cite

If you use this code in your research, please consider citing the work:

```bibtex
@misc{pixel2025renderer,
  title={PIXEL Renderer},
  author={Moryossef, Amit and Kesen, Ilker},
  howpublished={\url{https://github.com/sign/pixel-renderer}},
  year={2025}
}
```