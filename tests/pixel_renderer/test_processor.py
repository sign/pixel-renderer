"""Tests for PixelRendererProcessor."""

import tempfile

import numpy as np
import pytest
from transformers import ProcessorMixin

from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS_MINIMAL
from pixel_renderer.processor import PixelRendererProcessor


@pytest.fixture
def font_config():
    """Create a FontConfig with actual fonts from example."""
    # Use a minimal set of real fonts that will actually download
    return FontConfig(sources=FONTS_NOTO_SANS_MINIMAL)


class TestPixelRendererProcessor:
    """Test PixelRendererProcessor class."""

    def test_processor_initialization(self, font_config):
        """Test that PixelRendererProcessor can be initialized."""
        processor = PixelRendererProcessor(font=font_config)

        assert hasattr(processor, "fontconfig_path")
        assert processor.fontconfig_path is not None

    def test_processor_has_font_attribute(self, font_config):
        """Test that processor has font attribute."""
        processor = PixelRendererProcessor(font=font_config)

        # The font should be stored as an attribute
        assert hasattr(processor, "font")

    def test_processor_class_attributes(self):
        """Test PixelRendererProcessor class attributes."""
        assert PixelRendererProcessor.name == "pixel-renderer-processor"
        assert PixelRendererProcessor.attributes == []

    def test_processor_has_render_methods(self, font_config):
        """Test that processor has render methods."""
        processor = PixelRendererProcessor(font=font_config)

        assert hasattr(processor, "render_text")
        assert hasattr(processor, "render_text_image")
        assert callable(processor.render_text)
        assert callable(processor.render_text_image)

    def test_processor_render_text_returns_array(self, font_config):
        """Test that render_text returns a numpy array."""
        processor = PixelRendererProcessor(font=font_config)

        result = processor.render_text("Hello", block_size=16, font_size=12)

        assert isinstance(result, np.ndarray)
        assert result.shape == (16, 48, 3)

    def test_processor_render_text_image_returns_image(self, font_config):
        """Test that render_text_image returns a PIL Image."""
        processor = PixelRendererProcessor(font=font_config)

        result = processor.render_text_image("Hello", block_size=16, font_size=12)

        # Should return a PIL Image
        from PIL import Image

        assert isinstance(result, Image.Image)

    def test_processor_render_with_different_params(self, font_config):
        """Test rendering with different block sizes and font sizes."""
        processor = PixelRendererProcessor(font=font_config)

        # Test with different parameters
        result1 = processor.render_text("Test", block_size=16, font_size=12)
        result2 = processor.render_text("Test", block_size=32, font_size=24)

        assert isinstance(result1, np.ndarray)
        assert isinstance(result2, np.ndarray)
        # Different parameters should produce different sized outputs
        assert result1.shape != result2.shape

    def test_processor_save_and_load(self, font_config):
        """Test save_pretrained and from_pretrained workflow."""
        processor = PixelRendererProcessor(font=font_config)

        with tempfile.TemporaryDirectory() as temp_dir:
            # Save processor
            processor.save_pretrained(save_directory=temp_dir, push_to_hub=False)

            # Load processor
            new_processor = PixelRendererProcessor.from_pretrained(temp_dir)

            # Verify loaded processor has required attributes
            assert hasattr(new_processor, "fontconfig_path")
            assert hasattr(new_processor, "font")

            # Verify it can render
            result = new_processor.render_text("Test", block_size=16, font_size=12)
            assert isinstance(result, np.ndarray)

    def test_processor_renders_empty_string(self, font_config):
        """Test rendering empty string."""
        processor = PixelRendererProcessor(font=font_config)

        result = processor.render_text("", block_size=16, font_size=12)

        assert isinstance(result, np.ndarray)
        # Empty string should still produce an array (with minimal size)
        assert result.size > 0

    def test_processor_renders_unicode(self, font_config):
        """Test rendering Unicode text."""
        processor = PixelRendererProcessor(font=font_config)

        # Test with various Unicode characters
        result = processor.render_text("Hello 世界 🌍", block_size=16, font_size=12)

        assert isinstance(result, np.ndarray)
        assert result.shape[2] == 3  # RGB

    def test_processor_fontconfig_created_in_font_dir(self, font_config):
        """Test that fontconfig is created in the font directory."""
        processor = PixelRendererProcessor(font=font_config)

        # Check that fontconfig path points to font config_dir
        assert processor.fontconfig_path.parent == font_config.get_font_dir()

    def test_processor_render_preserves_aspect_ratio(self, font_config):
        """Test that rendered text maintains reasonable aspect ratios."""
        processor = PixelRendererProcessor(font=font_config)

        # Render short and long text
        short = processor.render_text("Hi", block_size=16, font_size=12)
        long = processor.render_text("Hello World Test", block_size=16, font_size=12)

        # Longer text should have larger width
        assert long.shape[1] > short.shape[1]

    def test_processor_can_be_used_by_others(self):
        class OtherProcessor(ProcessorMixin):
            attributes = []

            def __init__(self, renderer=None):
                super().__init__()
                if isinstance(renderer, dict):
                    renderer.pop("processor_class", None)
                    renderer = PixelRendererProcessor(**renderer)
                self.renderer = renderer

            def to_dict(self, **kwargs):
                output = {"processor_class": self.__class__.__name__}
                if self.renderer:
                    output["renderer"] = self.renderer.to_dict()
                return output

        font = FontConfig(sources=FONTS_NOTO_SANS_MINIMAL)
        renderer = PixelRendererProcessor(font=font)
        processor = OtherProcessor(renderer)

        with tempfile.TemporaryDirectory() as temp_dir:
            processor.save_pretrained(save_directory=temp_dir, push_to_hub=False)
            new_processor = OtherProcessor.from_pretrained(temp_dir)
            assert new_processor.renderer.font is not None
