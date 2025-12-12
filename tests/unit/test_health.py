from __future__ import annotations

import asyncio
from fastapi import FastAPI

from src.main import create_app
from src.api.health import health


def test_create_app_returns_fastapi_instance():
    app = create_app()
    assert isinstance(app, FastAPI)


def test_health_handler_returns_status_ok():
    result = asyncio.run(health())
    assert result == {"status": "ok"}
