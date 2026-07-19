from __future__ import annotations

import sys

from config import PROJECT_VERSION
from browser.manager import BrowserManager
from utils.console import clear_screen, pause, print_header
from utils.debug import clear_debug_directory
from utils.logger import configure_logging, get_logger


def browser_test() -> None:
    logger = get_logger()
    clear_debug_directory()
    manager = BrowserManager()

    try:
        logger.info("Starting browser test.")
        manager.start()
        manager.open_required_pages()
        manager.capture_startup_debug()

        print("\nBrowser test completed.")
        print("CentralReach and Outlook should now be open.")
        print("Log and screenshot files were written to debug/current/.")
        input("\nLog in manually if needed, then press ENTER here to close the automation browser...")
    except KeyboardInterrupt:
        logger.warning("Browser test interrupted by user.")
    except Exception as exc:
        logger.exception("Browser test failed: %s", exc)
        try:
            manager.capture_failure_debug(exc)
        except Exception:
            logger.exception("Could not capture failure debug package.")
        print("\nBrowser test failed.")
        print("Open debug/current/ and upload that folder or ZIP it for review.")
        pause()
    finally:
        manager.close()


def show_menu() -> str:
    clear_screen()
    print_header(f"CentralReach Automation v{PROJECT_VERSION}")
    print("1) Test browser and login persistence")
    print("2) Clear debug files")
    print("3) Show project paths")
    print("4) Exit")
    return input("\nChoice: ").strip()


def show_paths() -> None:
    from config import DEBUG_DIR, LOG_DIR, BROWSER_PROFILE_DIR, DOWNLOAD_DIR
    print("\nProject paths")
    print(f"Browser profile: {BROWSER_PROFILE_DIR}")
    print(f"Debug:           {DEBUG_DIR}")
    print(f"Logs:            {LOG_DIR}")
    print(f"Invoices:        {DOWNLOAD_DIR}")
    pause()


def main() -> int:
    configure_logging()

    while True:
        choice = show_menu()

        if choice == "1":
            browser_test()
        elif choice == "2":
            clear_debug_directory()
            print("\nDebug files cleared.")
            pause()
        elif choice == "3":
            show_paths()
        elif choice == "4":
            return 0
        else:
            print("\nInvalid choice.")
            pause()


if __name__ == "__main__":
    sys.exit(main())
