# PIXEL Renderer

This repository contains a text renderer for PIXEL models.

## Usage

Install dependencies:

```shell
conda create -n pixel python=3.12 -y
conda activate pixel
conda install -c conda-forge pycairo pygobject manimpango -y
pip install ".[dev]"
```

Install:

```bash
pip install pixel-renderer
```

Render text as an image (array):

```python
from pixel_renderer.renderer import render_text

render_text(text="test", block_size=16, dpi=120, font_size=12)
```

> [!CAUTION]
> Our text [renderer](./pixel_renderer/renderer.py) relies on the computer's font rendering capabilities.
> Rendering on different systems may yield different results (e.g. emoji).
> It is a work in progress to create a more robust renderer, decoupled from the system's font rendering,
> for better consistency across platforms and easier reproducibility.

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