from __future__ import annotations

import shutil

from config import AUTO_DELETE_PREVIOUS_DEBUG, DEBUG_DIR


def clear_debug_directory() -> None:
    if AUTO_DELETE_PREVIOUS_DEBUG and DEBUG_DIR.exists():
        shutil.rmtree(DEBUG_DIR)
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
