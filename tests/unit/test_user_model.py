from __future__ import annotations

import pytest
from sqlmodel import select

from src.models.user import User
from src.services import auth
from src.services.db import create_all, get_engine


@pytest.mark.anyio
async def test_user_persists_hashed_password(tmp_path) -> None:
    db_file = tmp_path / "user.db"
    engine = get_engine(f"sqlite+aiosqlite:///{db_file}")
    await create_all(engine)
    try:
        async with engine.begin() as conn:
            pwd_hash = auth.hash_password("pw123")
            result = await conn.execute(
                User.__table__.insert()
                .returning(User.id, User.username, User.password_hash),
                [{"username": "alice", "password_hash": pwd_hash}],
            )
            row = result.first()
            assert row.username == "alice"
            assert row.password_hash == pwd_hash
            assert auth.verify_password("pw123", row.password_hash)
    finally:
        await engine.dispose()


@pytest.mark.anyio
async def test_username_unique_constraint(tmp_path) -> None:
    db_file = tmp_path / "user_unique.db"
    engine = get_engine(f"sqlite+aiosqlite:///{db_file}")
    await create_all(engine)
    try:
        async with engine.begin() as conn:
            await conn.execute(
                User.__table__.insert(),
                [
                    {"username": "bob", "password_hash": auth.hash_password("pw1")},
                ],
            )
            with pytest.raises(Exception):
                await conn.execute(
                    User.__table__.insert(),
                    [{"username": "bob", "password_hash": auth.hash_password("pw2")}],
                )
    finally:
        await engine.dispose()
