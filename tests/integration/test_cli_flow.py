from __future__ import annotations

import builtins
from unittest import mock

import pytest

import src.main  # noqa: F401  # ensures app loads


@mock.patch("src.cli.menu.main_menu_loop")
def test_view_flow_entry_calls_menu_loop(mock_loop):
    # Simulate Typer entry invocation by calling entrypoint directly
    from src.main import entrypoint

    with mock.patch.object(builtins, "input", side_effect=EOFError()):
        entrypoint()

    mock_loop.assert_called_once()




@mock.patch("src.cli.menu.main_menu_loop")
def test_add_flow_menu_loop_called(mock_loop):
    from src.main import entrypoint
    with mock.patch.object(builtins, "input", side_effect=EOFError()):
        entrypoint()
    mock_loop.assert_called()





@mock.patch("src.cli.menu.main_menu_loop")
def test_manage_flow_menu_loop_called(mock_loop):
    from src.main import entrypoint
    with mock.patch.object(builtins, "input", side_effect=EOFError()):
        entrypoint()
    mock_loop.assert_called()
