from __future__ import annotations

import asyncio

from src.api.health import health


def test_health_endpoint_direct_call_returns_ok():
    result = asyncio.run(health())
    assert result == {"status": "ok"}
