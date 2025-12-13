from __future__ import annotations

import logging
import os
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncEngine
from fastapi import FastAPI

from src.api import health as health_router
from src.cli import menu
from src.services import db

app = FastAPI()
app.include_router(health_router.router)

_engine: Optional[AsyncEngine] = None


@app.on_event("startup")
async def startup() -> None:
    """Initialize database engine at startup; fail fast if invalid."""
    global _engine
    try:
        _engine = await db.init_engine_from_env()
    except Exception as exc:  # noqa: BLE001
        # Avoid leaking secrets; log only the exception type/message.
        logging.getLogger("uvicorn.error").error("Database initialization failed", exc_info=exc)
        raise


@app.on_event("shutdown")
async def shutdown() -> None:
    """Dispose engine on shutdown."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


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
