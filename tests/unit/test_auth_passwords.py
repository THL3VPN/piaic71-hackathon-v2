from __future__ import annotations

import pytest

from src.services import auth


def test_hash_and_verify_roundtrip() -> None:
    password = "s3cret!"
    hashed = auth.hash_password(password)
    assert hashed != password
    assert auth.verify_password(password, hashed)


def test_verify_fails_for_wrong_password() -> None:
    password = "s3cret!"
    hashed = auth.hash_password(password)
    assert not auth.verify_password("wrong", hashed)


def test_hash_is_not_deterministic(monkeypatch: pytest.MonkeyPatch) -> None:
    pwd = "abc123"
    first = auth.hash_password(pwd)
    second = auth.hash_password(pwd)
    assert first != second

