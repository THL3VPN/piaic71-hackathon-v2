from __future__ import annotations

import os
import runpy
from unittest import mock

from src.cli import app as app_module
from src.cli import menu
from src import main as main_module


def test_run_delegates_to_menu():
    with mock.patch.object(menu, "main_menu_loop") as mock_loop:
        app_module.run()
        mock_loop.assert_called_once_with()


def test_entrypoint_bypasses_typer_under_pytest():
    with mock.patch.dict(os.environ, {"PYTEST_CURRENT_TEST": "1"}):
        with mock.patch.object(menu, "main_menu_loop") as mock_loop:
            main_module.entrypoint()
            mock_loop.assert_called_once_with()


def test_main_callback_invokes_run_when_no_subcommand():
    ctx = mock.Mock()
    ctx.invoked_subcommand = None
    with mock.patch.object(menu, "main_menu_loop") as mock_loop:
        main_module.main(ctx)
        mock_loop.assert_called_once_with()


def test_entrypoint_invokes_app_when_not_testing():
    with mock.patch.dict(os.environ, {}, clear=True):
        with mock.patch.object(main_module, "app") as mock_app:
            main_module.entrypoint()
            mock_app.assert_called_once_with()


def test_main_guard_executes_entrypoint_under_pytest_env():
    with mock.patch.dict(os.environ, {"PYTEST_CURRENT_TEST": "1"}):
        with mock.patch.object(menu, "main_menu_loop") as mock_loop:
            runpy.run_path('src/main.py', run_name='__main__')
            mock_loop.assert_called_once_with()
