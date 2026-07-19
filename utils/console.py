from __future__ import annotations

import os


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def print_header(title: str) -> None:
    width = 58
    print("=" * width)
    print(title.center(width))
    print("=" * width)


def pause(message: str = "\nPress ENTER to continue...") -> None:
    input(message)
