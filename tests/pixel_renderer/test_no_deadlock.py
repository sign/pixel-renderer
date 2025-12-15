"""
Test for fontconfig fork-safety with PyTorch DataLoader.

These tests verify the fix for the deadlock issue described in:
https://github.com/sign/pixel-renderer/issues/13

The issue was that fontconfig (not fork-safe) was initialized in the parent
process, causing mutex deadlocks in forked workers.

The fix implements lazy initialization: fontconfig is only initialized when
first needed in each process, ensuring each fork gets clean state.

## Running the tests

Normal run (completes quickly):
    pytest tests/pixel_renderer/test_no_deadlock.py -v
"""

import multiprocessing as mp

import pytest
from torch.utils.data import DataLoader, Dataset

from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS_MINIMAL
from pixel_renderer.processor import PixelRendererProcessor


@pytest.fixture
def font_config():
    """Create a FontConfig with actual fonts from example."""
    return FontConfig(sources=FONTS_NOTO_SANS_MINIMAL)


@pytest.fixture
def processor(font_config):
    """Create a PixelRendererProcessor with fontconfig initialized."""
    return PixelRendererProcessor(font=font_config)


class TextRenderDataset(Dataset):
    """Simple dataset that renders text using PixelRendererProcessor."""

    def __init__(self, texts, processor):
        self.texts = texts
        self.processor = processor

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = self.texts[idx]
        # This is where the deadlock occurs in worker processes
        rendered = self.processor.render_text(text, block_size=16, font_size=12)
        return {
            'text': text,
            'rendered_shape': rendered.shape,
        }


def simulate_first_fork(processor, test_text="Hello from first fork"):
    """
    Simulate the first fork operation (like pack_dataset() does).
    This uses fontconfig in the forked process.
    """
    try:
        processor.render_text(test_text, block_size=16, font_size=12)
        return True
    except Exception:  # noqa: BLE001
        # Broad exception catch is intentional - we just want to know if rendering succeeded
        return False


def test_no_deadlock_with_dataloader_single_fork(processor):
    """
    Test that DataLoader with fork works without deadlock (single fork).

    With lazy initialization fix, fontconfig is initialized independently in
    each worker, so fork-based DataLoader works correctly.
    """
    texts = ["Hello World", "Test 1"]
    dataset = TextRenderDataset(texts, processor)

    # Single fork should work
    loader = DataLoader(
        dataset,
        batch_size=1,
        num_workers=1,
        multiprocessing_context=None,  # Use default fork
        timeout=10,
    )

    results = []
    for batch in loader:
        results.append(batch['text'][0])

    assert len(results) == len(texts)


def test_no_deadlock_with_dataloader_double_fork(processor):
    """
    Test that DataLoader with double fork doesn't deadlock.

    This test verifies the fix for issue #13 by simulating:
    1. First fork (like pack_dataset() from TRL)
    2. Second fork (PyTorch DataLoader with num_workers>0)

    With lazy initialization, each forked process initializes fontconfig
    independently, preventing mutex deadlocks.
    """
    texts = ["Hello", "World"]
    dataset = TextRenderDataset(texts, processor)

    # First fork (simulate pack_dataset)
    ctx = mp.get_context('fork')
    pool = ctx.Pool(processes=1)
    first_result = pool.apply(simulate_first_fork, (processor, "First fork"))
    pool.close()
    pool.join()

    assert first_result is True, "First fork should complete successfully"

    # Second fork (DataLoader) - with fix, this should work
    loader = DataLoader(
        dataset,
        batch_size=1,
        num_workers=1,
        multiprocessing_context=None,  # Use fork
        timeout=10,
    )

    results = []
    for batch in loader:
        results.append(batch['text'][0])

    assert len(results) == len(texts)


def test_no_deadlock_with_dataloader_spawn(processor):
    """
    Test that DataLoader with spawn works without deadlock.

    This test should PASS - spawn creates clean process state and avoids
    the fontconfig fork-safety issue.
    """
    texts = ["Hello World", "Test 1"]
    dataset = TextRenderDataset(texts, processor)

    # Spawn should always work
    ctx = mp.get_context('spawn')
    loader = DataLoader(
        dataset,
        batch_size=1,
        num_workers=1,
        multiprocessing_context=ctx,
        timeout=10,
    )

    results = []
    for batch in loader:
        results.append(batch['text'][0])

    assert len(results) == len(texts)
