from __future__ import annotations

import typer

from src.cli.app import run

app = typer.Typer(add_completion=False, no_args_is_help=False, rich_markup_mode="rich")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """Interactive CLI todo app."""
    # If invoked without subcommands, start the interactive loop
    if ctx.invoked_subcommand is None:
        run()


def entrypoint() -> None:
    """Entrypoint used by __main__ and tests."""
    # Avoid parsing pytest args; run loop directly when under test.
    import os
    if "PYTEST_CURRENT_TEST" in os.environ:
        run()
        return
    app()


if __name__ == "__main__":
    entrypoint()
