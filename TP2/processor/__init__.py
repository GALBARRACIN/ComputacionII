# processor/__init__.py
from __future__ import annotations

from .screenshot import generate_screenshot_base64, save_base64_to_file
from .performance import analyze_performance
from .image_processor import generate_thumbnails

def generate_screenshot(
    url: str,
    timeout_ms: int = 120_000,
    full_page: bool = True,
    viewport=(1280, 900),
    headless: bool = True,
):

    return generate_screenshot_base64(
        url,
        timeout_ms=timeout_ms,
        full_page=full_page,
        viewport=viewport,
        headless=headless,
    )

__all__ = [
    "generate_screenshot",
    "analyze_performance",
    "generate_thumbnails",
    "save_base64_to_file",
]

__version__ = "0.1.0"
