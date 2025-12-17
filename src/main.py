from __future__ import annotations

import logging
import os
from typing import Any, Optional
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

from src.api import health as health_router
from src.api import tasks as tasks_router
from src.api import auth as auth_router
from src.cli import menu
from src.services import auth
from src.services import db

_engine: Optional[AsyncEngine] = None

app = FastAPI()
frontend_origin = os.getenv("NEXT_PUBLIC_API_BASE_URL") or "http://localhost:3000"
allowed_origins = {
    frontend_origin.rstrip("/"),
    "http://localhost:3000",
    "http://127.0.0.1:3000",
}
# Ensure CORS headers are present even on auth failures (401/403):
# middleware are executed in reverse order of addition; the last added is outermost.
app.add_middleware(auth.AuthMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(allowed_origins),
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.include_router(health_router.router)
app.include_router(auth_router.router, prefix="/api")
app.include_router(tasks_router.router, prefix="/api")


@app.on_event("startup")
async def startup() -> None:
    """Initialize database engine at startup; fail fast if invalid."""
    try:
        engine = await db.init_engine_from_env()
        global _engine
        _engine = engine
    except Exception as exc:  # noqa: BLE001
        # Avoid leaking secrets; log only the exception type/message.
        logging.getLogger("uvicorn.error").error("Database initialization failed", exc_info=exc)
        raise


@app.on_event("shutdown")
async def shutdown() -> None:
    """Dispose engine on shutdown."""
    await db.dispose_engine()
    global _engine
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
