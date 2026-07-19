from pathlib import Path

PROJECT_VERSION = "0.2.0"
PROJECT_ROOT = Path(__file__).resolve().parent

# Browser behavior
HEADLESS = False
SLOW_MO_MS = 100
BROWSER_CHANNEL = "chrome"  # Falls back to bundled Chromium if Chrome is unavailable.
BROWSER_PROFILE_DIR = PROJECT_ROOT / "browser_profile"

# Pages opened by the browser test
CENTRALREACH_URL = "https://members.centralreach.com/#billingmanager/billing/"
OUTLOOK_URL = "https://outlook.cloud.microsoft/mail/"

# Output folders
LOG_DIR = PROJECT_ROOT / "logs"
DEBUG_DIR = PROJECT_ROOT / "debug" / "current"
STATE_DIR = PROJECT_ROOT / "state"
SCREENSHOT_DIR = DEBUG_DIR / "screenshots"
DOWNLOAD_DIR = PROJECT_ROOT / "invoices"

# Debug behavior
AUTO_DELETE_PREVIOUS_DEBUG = True
TAKE_STARTUP_SCREENSHOTS = True
FULL_PAGE_SCREENSHOTS = False
DEFAULT_TIMEOUT_MS = 30_000
