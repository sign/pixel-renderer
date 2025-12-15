from __future__ import annotations

import os

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

        # Store fontconfig setup parameters for lazy initialization
        # Don't initialize fontconfig here to avoid fork-safety issues
        self._font_dir = None
        self._fontconfig_path = None
        self._initialized_pid = None  # Track which process initialized fontconfig

        if self.font is not None:
            self._font_dir = font.get_font_dir()

    def _ensure_fontconfig_initialized(self) -> None:
        """
        Lazy initialization of fontconfig for fork-safety.

        This method ensures fontconfig is initialized in the current process
        before rendering. It's called on-demand, not in __init__, to prevent
        fork-safety issues.

        **Why this matters:**
        - Fontconfig uses internal mutexes (locks) to protect its data structures
        - When fork() creates a child process, it copies mutex state but not threads
        - If fontconfig was initialized in parent, child inherits broken mutex state
        - Child deadlocks when trying to acquire mutexes owned by non-existent threads

        **How this fixes it:**
        - Parent process: Never initializes fontconfig (stores config only)
        - Each child process: Initializes fontconfig independently on first render
        - Each process gets clean mutex state with no cross-process dependencies

        **When fontconfig gets initialized:**
        1. First time render_text() is called (never before)
        2. After fork (detects PID changed, re-initializes in new process)

        See: https://github.com/sign/pixel-renderer/issues/13
        """
        if self.font is None:
            raise ValueError("FontConfig must be provided to render text.")

        current_pid = os.getpid()

        # Initialize if not in this process yet
        # Covers: first time (None) or after fork (different PID)
        if self._initialized_pid != current_pid:
            # Initialize fontconfig fresh in THIS process
            font_configurator = FontConfigurator()
            self._fontconfig_path = font_configurator.setup_font(
                mode=FontconfigMode.TEMPLATE_MINIMAL,
                font_dir=self._font_dir,
                fontconfig_destination_dir=self._font_dir,
                force_reinitialize=True,
            )
            # Remember we initialized in this process
            self._initialized_pid = current_pid

    @property
    def fontconfig_path(self):
        """Get fontconfig path, initializing if necessary."""
        self._ensure_fontconfig_initialized()
        return self._fontconfig_path

    def render_text(self, text: str, block_size: int = 16, font_size: int = 12):
        """Render text to numpy array."""
        self._ensure_fontconfig_initialized()
        return render_text(text, block_size=block_size, font_size=font_size)

    def render_text_image(self, text: str, block_size: int = 16, font_size: int = 12):
        """Render text to PIL Image."""
        self._ensure_fontconfig_initialized()
        return render_text_image(text, block_size=block_size, font_size=font_size)

    def to_dict(self, **unused_kwargs):
        return {
            "font": self.font.to_dict(),
        }


# TODO: register to AutoProcessor instead
#  Using video processor as a workaround https://github.com/huggingface/transformers/issues/41816
AutoVideoProcessor.register(FontConfig, PixelRendererProcessor)
