# processor/screenshot.py
import base64
import logging
from typing import Dict, Any, Optional, Tuple

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

logger = logging.getLogger("processor.screenshot")
logger.addHandler(logging.NullHandler())


def generate_screenshot_base64(
    url: str,
    timeout_ms: int = 120_000,
    full_page: bool = False,
    viewport: Tuple[int, int] = (1280, 900),
    clip: Optional[Dict[str, int]] = None,
    headless: bool = True,
) -> Dict[str, Any]:
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=headless)
            page = browser.new_page(viewport={"width": viewport[0], "height": viewport[1]})
            page.set_default_navigation_timeout(timeout_ms)
            page.set_default_timeout(timeout_ms)

            logger.info("Navigating to %s with timeout %d ms", url, timeout_ms)
            page.goto(url, wait_until="networkidle", timeout=timeout_ms)
            page.wait_for_load_state("networkidle", timeout=timeout_ms)

            logger.info("Taking screenshot full_page=%s clip=%s", full_page, bool(clip))
            if clip:
                # clip requires full_page=False
                img_bytes = page.screenshot(clip=clip, full_page=False, timeout=timeout_ms)
            else:
                img_bytes = page.screenshot(full_page=full_page, timeout=timeout_ms)

            browser.close()

            b64 = base64.b64encode(img_bytes).decode("ascii")
            return {"data": b64}
    except PWTimeout:
        logger.warning("Playwright timeout while capturing %s", url)
        return {"error": "screenshot_timeout"}
    except Exception as exc:
        logger.exception("Unexpected error generating screenshot for %s", url)
        return {"error": "other", "detail": str(exc)}


def save_base64_to_file(b64: str, path: str) -> None:
    with open(path, "wb") as f:
        f.write(base64.b64decode(b64))
