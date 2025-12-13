from __future__ import annotations

from src.cli import app


def test_run_invokes_menu(monkeypatch) -> None:
    called = []
    monkeypatch.setattr(app.menu, "main_menu_loop", lambda: called.append("ok"))
    app.run()
    assert called == ["ok"]
