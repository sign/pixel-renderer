import unittest

import numpy as np
import torch

from pixel_renderer import render_text


class TestRenderer(unittest.TestCase):
    def test_single_text_has_black_pixels(self):
        """Test that rendering a single text produces black pixels in the image."""
        text = "Hello World"
        arr = render_text(text, block_size=32, font_size=20)

        # Check if there are any black pixels (0, 0, 0) in RGB
        # Since the background is white (255, 255, 255), any text should create non-white pixels
        has_black_pixels = np.any(arr < 255)

        assert has_black_pixels, "Rendered text should contain black pixels"

    def test_empty_text_no_black_pixels(self):
        """Test that rendering empty text produces no black pixels (all white)."""
        arr = render_text("", block_size=32, font_size=20)

        # Check that all pixels are white (255, 255, 255)
        all_white = np.all(arr == 255)

        assert all_white, "Empty text should produce an all-white image"

    def test_multiple_different_texts_are_different(self):
        """Test that different texts produce different renders."""
        texts = ["a", "b"]
        renders = [render_text(text, block_size=32, font_size=20) for text in texts]
        tensors = [torch.tensor(arr) for arr in renders]

        # Check that the two renders are different
        are_different = not torch.equal(tensors[0], tensors[1])

        assert are_different, "Different texts 'a' and 'b' should produce different renders"

    def test_multiple_identical_texts_deconstruction(self):
        """Test that identical texts produce identical renders."""
        texts = ["a", "a", "a", "a"]
        renders = [render_text(text, block_size=32, font_size=20) for text in texts]
        tensors = [torch.tensor(arr) for arr in renders]

        # All renders should be identical since they contain the same text
        first = tensors[0]
        all_same = all(torch.equal(first, t) for t in tensors[1:])

        assert all_same, "Identical texts 'a' should produce identical renders"

    def test_render_consistency(self):
        """Test that rendering the same text multiple times produces consistent results."""
        text = "consistent test"

        # Render the same text twice
        arr1 = render_text(text, block_size=32, font_size=20)
        arr2 = render_text(text, block_size=32, font_size=20)

        # Check that both renderings are identical
        are_identical = np.array_equal(arr1, arr2)

        assert are_identical, "Rendering the same text should produce identical results"

    def test_newline_text_has_black_pixels(self):
        """Test that newline character renders with visible content."""
        arr = render_text("\n", block_size=32, font_size=20)

        # Check if there are any black pixels (0, 0, 0) in RGB
        # Since the background is white (255, 255, 255), any text should create non-white pixels
        has_black_pixels = np.any(arr < 255)

        assert has_black_pixels, "Rendered text should contain black pixels"

    def test_signwriting_renders_correctly(self):
        """Test that SignWriting text renders with correct dimensions and content."""
        text = "𝠀񀀒񀀚񋚥񋛩𝠃𝤟𝤩񋛩𝣵𝤐񀀒𝤇𝣤񋚥𝤐𝤆񀀚𝣮𝣭"
        block_size = 32
        arr = render_text(text, block_size=block_size, font_size=20)

        # Validate array is 3D (height, width, channels)
        assert arr.ndim == 3, f"Expected 3D array, got {arr.ndim}D with shape {arr.shape}"
        height, width, channels = arr.shape

        # Validate channels (RGB)
        assert channels == 3, f"Expected 3 channels (RGB), got {channels}"

        # Validate dimensions are multiples of block_size
        assert height % block_size == 0, f"Height {height} is not a multiple of block_size {block_size}"
        assert width % block_size == 0, f"Width {width} is not a multiple of block_size {block_size}"

        # Validate array is contiguous (important for downstream processing)
        assert arr.flags["C_CONTIGUOUS"], f"Array should be C-contiguous, strides: {arr.strides}"

        # Check if the image contains non-white pixels (content was actually rendered)
        has_non_white_pixels = np.any(arr < 255)
        assert has_non_white_pixels, "Rendered signwriting should contain non-white pixels"

    def test_render_text_has_no_negative_indexes(self):
        arr = render_text("hello")

        # basic sanity
        assert isinstance(arr, np.ndarray), f"expected ndarray-ish, got {type(arr)}"

        # no negative strides (torch.from_numpy would accept)
        assert not np.any(np.array(arr.strides) < 0), f"negative stride found: {arr.strides}"

    def test_render_varying_lengths_shape_correctness(self):
        """Test that rendering 1 to 100 letters produces correct shapes.

        This test verifies that optimizations (surface pooling, layout reuse)
        don't break the output dimensions for varying text lengths.
        """
        block_size = 16
        font_size = 12
        alphabet = "abcdefghijklmnopqrstuvwxyz"

        prev_width = 0
        for length in range(1, 101):
            # Create text of specified length by repeating alphabet
            text = (alphabet * ((length // len(alphabet)) + 1))[:length]
            assert len(text) == length

            arr = render_text(text, block_size=block_size, font_size=font_size)

            # Check shape: (height, width, channels)
            assert arr.ndim == 3, f"Length {length}: expected 3D array, got {arr.ndim}D"
            height, width, channels = arr.shape

            # Height should equal block_size
            assert height == block_size, f"Length {length}: height {height} != block_size {block_size}"

            # Channels should be 3 (RGB)
            assert channels == 3, f"Length {length}: channels {channels} != 3"

            # Width should be a multiple of block_size
            assert width % block_size == 0, f"Length {length}: width {width} not multiple of {block_size}"

            # Width should be positive
            assert width > 0, f"Length {length}: width should be positive"

            # Longer text should generally produce wider images (with some tolerance for block alignment)
            # We check that width doesn't decrease as text gets longer
            assert width >= prev_width, f"Length {length}: width {width} < previous width {prev_width}"
            prev_width = width

            # Should contain non-white pixels (text was actually rendered)
            has_content = np.any(arr < 255)
            assert has_content, f"Length {length}: rendered text should contain non-white pixels"

            # Array should be contiguous (important for downstream processing)
            assert arr.flags['C_CONTIGUOUS'], f"Length {length}: array should be C-contiguous"

            # No negative strides
            assert all(s >= 0 for s in arr.strides), f"Length {length}: negative stride found: {arr.strides}"

        # Validate final width for 100 characters is reasonable
        # At font_size=12, each character is ~6-7px, so 100 chars ≈ 600-700px + 10px padding
        assert 500 < prev_width < 700

if __name__ == "__main__":
    unittest.main()
