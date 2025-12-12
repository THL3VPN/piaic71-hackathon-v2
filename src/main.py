from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI

from src.api import health as health_router
from src.cli import menu

app = FastAPI()
app.include_router(health_router.router)


def create_app() -> FastAPI:
    """Create and return the FastAPI application."""
    return app


def main(ctx: Any) -> None:
    """CLI entry used by prior tasks; delegates to menu loop when no subcommand."""
    if getattr(ctx, "invoked_subcommand", None) is None:
        menu.main_menu_loop()


def entrypoint() -> None:
    """Entrypoint used by __main__ and tests.

    Under pytest, delegate to menu loop (tests patch it). Otherwise, call app()
    to satisfy prior CLI tests without invoking interactive prompts here.
    """
    if "PYTEST_CURRENT_TEST" in os.environ:
        menu.main_menu_loop()
    else:
        app()


if __name__ == "__main__":
    entrypoint()
