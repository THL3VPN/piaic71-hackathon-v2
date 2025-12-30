from __future__ import annotations

# [Task]: T002 [From]: specs/008-chat-storage/spec.md User Story 1

import base64
import hashlib
import hmac
import json
import os
import sys
from pathlib import Path
from typing import Iterator

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


# Ensure project root is importable in tests.
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Default DB env so DB tests run locally without extra exports.
os.environ.setdefault("RUN_DB_TESTS", "1")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

from src.services import db  # noqa: E402


@pytest.fixture
def test_secret(monkeypatch: pytest.MonkeyPatch) -> str:
    secret = os.getenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    monkeypatch.setenv("BETTER_AUTH_SECRET", secret)
    return secret


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


@pytest.fixture
def token_factory(test_secret: str):
    def _build(sub: str = "test-user", extra: dict | None = None) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {"sub": sub}
        if extra:
            payload.update(extra)
        header_b64 = _b64(json.dumps(header, separators=(",", ":")).encode())
        payload_b64 = _b64(json.dumps(payload, separators=(",", ":")).encode())
        signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
        signature = hmac.new(
            test_secret.encode("utf-8"), signing_input, hashlib.sha256
        ).digest()
        signature_b64 = _b64(signature)
        return ".".join([header_b64, payload_b64, signature_b64])

    return _build


@pytest.fixture
def auth_headers_factory(token_factory):
    def _headers(sub: str = "test-user", extra: dict | None = None) -> dict[str, str]:
        token = token_factory(sub=sub, extra=extra)
        return {"Authorization": f"Bearer {token}"}

    return _headers


@pytest.fixture
async def engine(tmp_path, monkeypatch: pytest.MonkeyPatch) -> AsyncEngine:
    db_file = tmp_path / "test.db"
    url = f"sqlite+aiosqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", url)
    engine = db.get_engine(url)
    await db.create_all(engine)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> Iterator[AsyncSession]:
    async with db.get_session_for_engine(engine) as sess:
        yield sess
