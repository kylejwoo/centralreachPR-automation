from __future__ import annotations

import json
import platform
import traceback
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.sync_api import BrowserContext, Page, Playwright, sync_playwright

from config import (
    BROWSER_CHANNEL,
    BROWSER_PROFILE_DIR,
    CENTRALREACH_URL,
    DEFAULT_TIMEOUT_MS,
    DOWNLOAD_DIR,
    FULL_PAGE_SCREENSHOTS,
    HEADLESS,
    OUTLOOK_URL,
    SCREENSHOT_DIR,
    SLOW_MO_MS,
    TAKE_STARTUP_SCREENSHOTS,
)
from utils.logger import get_logger


@dataclass
class ManagedPages:
    centralreach: Optional[Page] = None
    outlook: Optional[Page] = None


class BrowserManager:
    def __init__(self) -> None:
        self.logger = get_logger()
        self.playwright: Optional[Playwright] = None
        self.context: Optional[BrowserContext] = None
        self.pages = ManagedPages()

    def start(self) -> None:
        BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
        DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

        self.playwright = sync_playwright().start()

        launch_args = dict(
            user_data_dir=str(BROWSER_PROFILE_DIR),
            headless=HEADLESS,
            slow_mo=SLOW_MO_MS,
            accept_downloads=True,
            downloads_path=str(DOWNLOAD_DIR),
            viewport={"width": 1440, "height": 900},
        )

        try:
            self.context = self.playwright.chromium.launch_persistent_context(
                channel=BROWSER_CHANNEL,
                **launch_args,
            )
            self.logger.info("Launched persistent %s browser context.", BROWSER_CHANNEL)
        except Exception as chrome_error:
            self.logger.warning(
                "Could not launch Chrome channel (%s). Falling back to bundled Chromium. Error: %s",
                BROWSER_CHANNEL,
                chrome_error,
            )
            launch_args.pop("downloads_path", None)
            self.context = self.playwright.chromium.launch_persistent_context(**launch_args)
            self.logger.info("Launched persistent bundled Chromium context.")

        self.context.set_default_timeout(DEFAULT_TIMEOUT_MS)

    def open_required_pages(self) -> None:
        if self.context is None:
            raise RuntimeError("Browser context has not been started.")

        self.pages.centralreach = self._find_or_open_page(CENTRALREACH_URL, "centralreach")
        self.pages.outlook = self._find_or_open_page(OUTLOOK_URL, "outlook")

        self.pages.centralreach.bring_to_front()
        self.logger.info("CentralReach page ready: %s", self.pages.centralreach.url)
        self.logger.info("Outlook page ready: %s", self.pages.outlook.url)

    def _find_or_open_page(self, url: str, keyword: str) -> Page:
        assert self.context is not None

        for page in self.context.pages:
            if keyword.lower() in page.url.lower():
                self.logger.info("Reusing existing %s page.", keyword)
                return page

        page = self.context.new_page()
        self.logger.info("Opening %s: %s", keyword, url)
        page.goto(url, wait_until="domcontentloaded")
        return page

    def capture_startup_debug(self) -> None:
        if not TAKE_STARTUP_SCREENSHOTS:
            return

        if self.pages.centralreach:
            self._safe_screenshot(self.pages.centralreach, "centralreach_ready.png")
        if self.pages.outlook:
            self._safe_screenshot(self.pages.outlook, "outlook_ready.png")

        self._write_browser_state("browser_state.json")

    def capture_failure_debug(self, exc: Exception) -> None:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

        active_page = None
        if self.context and self.context.pages:
            active_page = self.context.pages[-1]

        if active_page:
            self._safe_screenshot(active_page, "failure.png")
            try:
                (SCREENSHOT_DIR.parent / "failure_page.html").write_text(
                    active_page.content(), encoding="utf-8"
                )
            except Exception:
                self.logger.exception("Could not save failure page HTML.")

        (SCREENSHOT_DIR.parent / "traceback.txt").write_text(
            "".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
            encoding="utf-8",
        )
        self._write_browser_state("failure_state.json")

    def _safe_screenshot(self, page: Page, filename: str) -> None:
        path = SCREENSHOT_DIR / filename
        try:
            page.screenshot(path=str(path), full_page=FULL_PAGE_SCREENSHOTS)
            self.logger.info("Saved screenshot: %s", path)
        except Exception:
            self.logger.exception("Failed to save screenshot: %s", path)

    def _write_browser_state(self, filename: str) -> None:
        data = {
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "platform": platform.platform(),
            "pages": [
                {"title": self._safe_title(page), "url": page.url}
                for page in (self.context.pages if self.context else [])
            ],
        }
        path = SCREENSHOT_DIR.parent / filename
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.logger.info("Saved browser state: %s", path)

    @staticmethod
    def _safe_title(page: Page) -> str:
        try:
            return page.title()
        except Exception:
            return ""

    def close(self) -> None:
        if self.context is not None:
            try:
                self.context.close()
            except Exception:
                self.logger.exception("Error while closing browser context.")
            finally:
                self.context = None

        if self.playwright is not None:
            try:
                self.playwright.stop()
            except Exception:
                self.logger.exception("Error while stopping Playwright.")
            finally:
                self.playwright = None
