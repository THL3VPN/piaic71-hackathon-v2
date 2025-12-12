from __future__ import annotations

from src.cli import menu


def run() -> None:
    """Main loop entry; delegates to menu loop."""
    menu.main_menu_loop()
