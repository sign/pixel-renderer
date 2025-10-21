# Copyright 2025- Pavel Stepachev
# SPDX-License-Identifier: Apache-2.0
import concurrent.futures
import json
import logging
import pathlib
import shutil

import requests  # type: ignore[import]

from font_download.tools import FontEntity, FontSource, ReproducibleFontDownloadUtils


class ReproducibleFontDownload:
    def __init__(self, cache_dir: str | pathlib.Path = ".cache/pixel_renderer/fonts") -> None:
        self.logger = logging.getLogger(__name__)
        self.cache_dir = self._create_cache_dir(path_to_dir=cache_dir)
        self.configs_dir = self._create_subdir_in_cache_dir("configs")

    def _create_cache_dir(self, path_to_dir: str | pathlib.Path) -> pathlib.Path:
        if not isinstance(path_to_dir, pathlib.Path):
            path_to_dir = pathlib.Path(path_to_dir)
        path_to_dir.mkdir(parents=True, exist_ok=True)
        return path_to_dir

    def _create_subdir_in_cache_dir(self, subdir_name: str) -> pathlib.Path:
        subdir_path = self.cache_dir.joinpath(subdir_name)
        subdir_path.mkdir(parents=True, exist_ok=True)
        return subdir_path

    def _download_file(self, url: str, dest_path: pathlib.Path) -> bool:
        """Download a file from URL to destination path."""
        self.logger.debug("Downloading file from %s", url)

        try:
            with requests.get(url, stream=True, timeout=30) as response:
                response.raise_for_status()

                # get content length for progress tracking (optional)
                total_size = int(response.headers.get("content-length", 0))  # noqa: F841

                with dest_path.open("wb") as f:
                    # larger chunk size for better throughput
                    for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                        if chunk:  # filter out keep-alive chunks
                            f.write(chunk)

            self.logger.debug("Successfully downloaded file to %s", dest_path)
        except requests.RequestException:
            self.logger.exception("Failed to download file from %s", url)
            if dest_path.exists():
                dest_path.unlink()
            return False
        else:
            return True

    def _download_font_parallel(self, source: FontSource, fonts_dir: pathlib.Path) -> FontEntity | None:
        """Download a single font (helper for parallel downloads)."""
        font_path = fonts_dir.joinpath(source.name)

        if self._download_file(url=source.url, dest_path=font_path):
            return FontEntity(name=source.name, url=source.url, file_path=font_path)

        self.logger.warning("Failed to download font: %s", source.name)
        return None

    def _verify_font_integrity(self, font_path: pathlib.Path, expected_sha256: str) -> bool:
        """Verify font file integrity using SHA256 hash."""
        try:
            actual_sha256 = ReproducibleFontDownloadUtils.compute_sha256(font_path)
            if actual_sha256 != expected_sha256:
                self.logger.warning(
                    "SHA256 mismatch for %s. Expected: %s, Got: %s", font_path.name, expected_sha256, actual_sha256
                )
                return False

            else:  # noqa: RET505
                self.logger.debug("SHA256 verified for %s", font_path.name)
                return True
        except FileNotFoundError:
            return False

    def _save_config_file(self, config_path: pathlib.Path, font_entities: list[FontEntity]) -> None:
        """Save configuration to JSON file."""
        config_data = [entity.to_config_format_dict() for entity in font_entities]
        try:
            with config_path.open("w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4)
            self.logger.info("Configuration saved to %s", config_path)
        except OSError:
            self.logger.exception("Failed to save configuration to %s", config_path)
            raise

    def _load_config_file(self, config_path: pathlib.Path) -> list[dict]:
        """Load configuration from JSON file."""
        if not config_path.exists():
            msg = f"Configuration file not found: {config_path}"
            self.logger.error(msg)
            raise FileNotFoundError(msg)

        try:
            with config_path.open("r", encoding="utf-8") as f:
                config_data = json.load(f)
        except json.JSONDecodeError:
            self.logger.exception("Invalid JSON in config file: %s", config_path)
            raise
        except OSError:
            self.logger.exception("Failed to read config file: %s", config_path)
            raise
        else:
            # only executes if no exception occurred
            self.logger.debug("Loaded configuration from %s", config_path)
            return config_data

    def resolve_config_path(self, config_name_or_path: str | pathlib.Path) -> pathlib.Path:
        """Resolve config name or path to actual config file path."""
        if isinstance(config_name_or_path, str):
            config_name_or_path = pathlib.Path(config_name_or_path)

        # if it's an absolute path or relative path that exists, use it directly
        if config_name_or_path.is_absolute() or config_name_or_path.exists():
            return config_name_or_path.with_suffix(".json")

        # otherwise, look in the configs directory
        config_path = self.configs_dir.joinpath(config_name_or_path).with_suffix(".json")
        return config_path  # noqa: RET504

    def save_config(
        self,
        sources: list[FontSource],
        config_name: str,
        dest_dir: str | pathlib.Path | None = None,
        max_workers: int = 5,
    ) -> pathlib.Path:
        """
        Download fonts and save configuration.

        Args:
            sources: List of FontSource objects to download
            config_name: Name for the configuration
            dest_dir: Optional custom directory for config file (default: cache/configs)
            max_workers: Maximum number of parallel downloads (default: 5)

        Returns:
            Path to the saved configuration file
        """
        if dest_dir is None:
            dest_dir = self.configs_dir
        else:
            if not isinstance(dest_dir, pathlib.Path):
                dest_dir = pathlib.Path(dest_dir)
            dest_dir.mkdir(parents=True, exist_ok=True)

        config_path = dest_dir.joinpath(config_name).with_suffix(".json")
        fonts_dir = self._create_subdir_in_cache_dir(subdir_name=config_name)

        font_entities: list[FontEntity] = []

        # parallel downloading
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_source = {
                executor.submit(self._download_font_parallel, source, fonts_dir): source for source in sources
            }

            for future in concurrent.futures.as_completed(future_to_source):
                result = future.result()
                if result:
                    font_entities.append(result)

        if not font_entities:
            msg = "No fonts were successfully downloaded"
            raise RuntimeError(msg)

        self._save_config_file(config_path=config_path, font_entities=font_entities)
        self.logger.info("Successfully saved %d fonts to config: %s", len(font_entities), config_name)

        return config_path

    def from_config(  # noqa: C901
        self,
        config_name_or_path: str | pathlib.Path,
        *,
        force_download: bool = False,
        max_workers: int = 5,
    ) -> pathlib.Path:
        """
        Load fonts from configuration.

        Downloads missing fonts and verifies integrity of existing ones.

        Args:
            config_name_or_path: Config name (e.g., "my_fonts") or path to config file
            force_download: If True, re-download all fonts even if they exist
            max_workers: Maximum number of parallel downloads (default: 5)

        Returns:
            Path to the directory containing all fonts

        Example:
            >>> downloader = ReproducibleFontDownload()
            >>> fonts_dir = downloader.from_config("my_fonts")
            >>> fonts_dir = downloader.from_config("/path/to/config.json")
        """
        config_path = self.resolve_config_path(config_name_or_path)
        config_data = self._load_config_file(config_path)

        # extract config name from the file name
        config_name = config_path.stem
        fonts_dir = self._create_subdir_in_cache_dir(subdir_name=config_name)

        # separate fonts into those needing download and those already cached
        fonts_to_download = []
        fonts_already_cached = []

        for item in config_data:
            try:
                font_name = item["name"]
                font_url = item["url"]  # noqa: F841
                expected_sha256 = item.get("sha256", "")
                font_path = fonts_dir.joinpath(font_name)

                should_download = force_download or not font_path.exists()

                # verify integrity if file exists and we're not forcing download
                if not should_download and expected_sha256:  # noqa: SIM102
                    if not self._verify_font_integrity(font_path, expected_sha256):
                        self.logger.warning("Font %s failed integrity check, re-downloading", font_name)
                        should_download = True

                if should_download:
                    fonts_to_download.append(item)
                else:
                    fonts_already_cached.append(font_name)
                    self.logger.debug("Font %s already exists and is valid", font_name)

            except (KeyError, TypeError):  # noqa: PERF203
                self.logger.exception("Invalid font entry in config")
                continue

        # download fonts in parallel
        fonts_downloaded = 0
        if fonts_to_download:

            def download_font_with_verification(item: dict) -> bool:
                font_name = item["name"]
                font_url = item["url"]
                expected_sha256 = item.get("sha256", "")
                font_path = fonts_dir.joinpath(font_name)

                self.logger.debug("Downloading font: %s", font_name)
                if self._download_file(url=font_url, dest_path=font_path):
                    # verify downloaded file if hash is provided
                    if expected_sha256:  # noqa: SIM102
                        if not self._verify_font_integrity(font_path, expected_sha256):
                            self.logger.error("Downloaded font %s failed integrity check", font_name)
                            font_path.unlink()
                            return False
                    return True
                else:  # noqa: RET505
                    self.logger.error("Failed to download font: %s", font_name)
                    return False

            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(download_font_with_verification, item): item for item in fonts_to_download}

                for future in concurrent.futures.as_completed(futures):
                    if future.result():
                        fonts_downloaded += 1

        fonts_processed = len(fonts_already_cached) + fonts_downloaded
        self.logger.info("Fonts ready in %s (%d total, %d downloaded)", fonts_dir, fonts_processed, fonts_downloaded)
        return fonts_dir

    @classmethod
    def from_sources(
        cls,
        sources: list[FontSource],
        config_name: str,
        cache_dir: str | pathlib.Path | None = ".cache/pixel_renderer/fonts",
    ) -> pathlib.Path:
        """
        Convenience method to create config and return fonts directory in one step.

        Args:
            sources: List of FontSource objects
            config_name: Name for the configuration
            cache_dir: Cache directory path

        Returns:
            Path to the directory containing all fonts
        """
        if cache_dir is None:
            cache_dir = ".cache/pixel_renderer/fonts"

        instance = cls(cache_dir=cache_dir)
        instance.save_config(sources=sources, config_name=config_name)
        return instance.from_config(config_name)

    def clear_cache(
        self,
        config_name: str | None = None,
        *,
        remove_configs: bool = False,
    ) -> None:
        """
        Clear cached fonts and optionally config files.

        Args:
            config_name: If provided, only clear fonts for this specific config.
                        If None, clear all cached fonts.
            remove_configs: If True, also remove config files

        Example:
            >>> downloader = ReproducibleFontDownload()
            >>> downloader.clear_cache("my_fonts")  # Clear only my_fonts
            >>> downloader.clear_cache()  # Clear all fonts
            >>> downloader.clear_cache(remove_configs=True)  # Clear everything
        """
        if config_name:
            # clear specific config's fonts
            fonts_dir = self.cache_dir.joinpath(config_name)
            if fonts_dir.exists():
                shutil.rmtree(fonts_dir)
                self.logger.info("Cleared fonts for config: %s", config_name)

            if remove_configs:
                config_path = self.configs_dir.joinpath(config_name).with_suffix(".json")
                if config_path.exists():
                    config_path.unlink()
                    self.logger.info("Removed config file: %s.json", config_name)
        else:
            # clear all fonts (but preserve configs directory structure)
            for item in self.cache_dir.iterdir():
                if item.is_dir() and item.name != "configs":
                    shutil.rmtree(item)
                    self.logger.info("Cleared all cached fonts: %s", item.name)

            if remove_configs and self.configs_dir.exists():
                shutil.rmtree(self.configs_dir)
                self._create_subdir_in_cache_dir("configs")
                self.logger.info("Cleared all config files")

    def list_configs(self) -> list[str]:
        """
        List all available configuration names.

        Returns:
            List of configuration names (without .json extension)
        """
        if not self.configs_dir.exists():
            return []

        configs = [config_file.stem for config_file in self.configs_dir.glob("*.json")]
        return sorted(configs)
