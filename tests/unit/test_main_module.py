from __future__ import annotations

import os

import pytest

from src import main


@pytest.mark.anyio
async def test_startup_and_shutdown_use_db(monkeypatch) -> None:
    class DummyEngine:
        disposed = False

        async def dispose(self) -> None:
            self.disposed = True

    async def fake_init_engine_from_env() -> DummyEngine:
        return DummyEngine()

    monkeypatch.setattr(main.db, "init_engine_from_env", fake_init_engine_from_env)

    await main.startup()
    assert isinstance(main._engine, DummyEngine)

    await main.shutdown()
    assert main._engine is None


def test_create_app_returns_module_app() -> None:
    assert main.create_app() is main.app


def test_main_delegates_to_menu(monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(main.menu, "main_menu_loop", lambda: calls.append("called"))

    class Ctx:
        invoked_subcommand = None

    main.main(Ctx())
    assert calls == ["called"]


def test_entrypoint_prefers_pytest_env(monkeypatch) -> None:
    calls: list[str] = []
    monkeypatch.setattr(main.menu, "main_menu_loop", lambda: calls.append("called"))
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "1")
    main.entrypoint()
    assert calls == ["called"]
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)


@pytest.mark.anyio
async def test_startup_logs_and_raises_on_failure(monkeypatch, caplog) -> None:
    async def fake_init_engine_from_env() -> None:
        raise RuntimeError("boom")

    monkeypatch.setattr(main.db, "init_engine_from_env", fake_init_engine_from_env)

    with caplog.at_level("ERROR"):
        with pytest.raises(RuntimeError):
            await main.startup()
    assert any("Database initialization failed" in rec.message for rec in caplog.records)
