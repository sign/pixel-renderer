"""
Benchmark script for pixel_renderer.render_text()

Usage:
    python examples/pixel_renderer/benchmark.py
"""

from tqdm import tqdm

from font_download import FontConfig
from font_download.example_fonts.noto_sans import FONTS_NOTO_SANS
from pixel_renderer import PixelRendererProcessor

# Sample words representative of real usage (mix of languages, lengths, special chars)
SAMPLE_WORDS = [
    "Hello", "World", "the", "a", "is", "of", "and", "to", "in", "that",
    "שלום", "עולם", "את", "של", "על", "עם", "לא", "הוא", "היא", "זה",
    "I", "you", "we", "they", "it", "be", "have", "do", "say", "get",
    "make", "go", "know", "take", "see", "come", "think", "look", "want", "give",
    "use", "find", "tell", "ask", "work", "seem", "feel", "try", "leave", "call",
    "<en>", "<he>", "\x0E", "\x0F",  # Special tokens
    ".", ",", "!", "?", ":", ";", "-", "(", ")", '"',
    "hello!", "world.", "test,", "foo-bar", "(test)", '"quoted"',
    "אבגדהוזחטיכלמנסעפצקרשת",  # Hebrew alphabet
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",  # English alphabet
    "0123456789",  # Numbers
    " ",  # Space
]

font_config = FontConfig(sources=FONTS_NOTO_SANS)
renderer = PixelRendererProcessor(font=font_config)

# Show sample render shape
print(f"Sample render shape: {renderer.render_text('Hello').shape}")

# Benchmark: ~110k it/s on Apple M1
for _ in tqdm(range(1000000)):
    word = SAMPLE_WORDS[_ % len(SAMPLE_WORDS)]
    renderer.render_text(word)
