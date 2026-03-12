import os
from pathlib import Path
from talon import Context, Module, actions

REPO_DIR = Path(__file__).parent.parent.parent


mod = Module()
mod.list(
    "edit_text_file",
    desc="Paths to frequently edited files (Talon list, CSV, etc.)",
)

ctx_win = Context()
ctx_win.matches = "os: windows"


@mod.action_class
class Actions:
    @staticmethod
    def edit_text_file(file: str):
        """Tries to open a file in the user's preferred text editor."""


@ctx_win.action_class("user")
class WinActions:
    @staticmethod
    def edit_text_file(file: str):
        path = get_full_path(file)
        actions.user.exec(f"code {path}")
        actions.user.wait_for_title_change()
        actions.edit.file_end()


def get_full_path(file: str) -> Path:
    path = Path(file).expanduser()
    if not path.is_absolute():
        path = REPO_DIR / path
    return path.resolve()
