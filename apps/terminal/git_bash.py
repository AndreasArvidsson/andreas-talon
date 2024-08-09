from talon import Module, Context, actions
import re

mod = Module()

mod.apps.git_bash = r"""
app: windows_terminal
and win.title: /MINGW64:/i
"""
mod.apps.git_bash = r"""
os: windows
and app.exe: mintty.exe
"""
mod.apps.git_bash = r"""
os: windows
app: vscode
win.file_ext: .bashbook
"""

ctx = Context()
ctx.matches = r"""
app: git_bash

app: git_bash
and app: windows_terminal


app: vscode
and win.title: /\[Terminal\]$/
"""

ctx.tags = ["terminal", "user.bash"]


@ctx.action_class("main")
class MainActions:
    def insert(text: str):
        text = convert_windows_system_paths(text)
        actions.next(text)


@ctx.action_class("edit")
class EditActions:
    def paste():
        text = actions.clip.text()
        updated_text = convert_windows_system_paths(text)
        if text != updated_text:
            actions.clip.set_text(updated_text)
        actions.next()


def convert_windows_system_paths(text: str) -> str:
    return re.sub(
        r"[a-zA-Z]:\\[\S]+", lambda m: convert_windows_system_path(m[0]), text
    )


def convert_windows_system_path(path: str) -> str:
    return "/" + path[0] + path[2:].replace("\\", "/")


@ctx.action_class("user")
class UserActions:
    def talon_app() -> str:
        return update_path(actions.next())

    def talon_home() -> str:
        return update_path(actions.next())

    def talon_user() -> str:
        return update_path(actions.next())

    def user_home() -> str:
        return update_path(actions.next())

    def file_manager_go(path: str):
        if path.startswith("shell:"):
            actions.insert(f"start {path}")
            actions.key("enter")
            return
        path = update_path(path)
        actions.next(path)


def update_path(path: str) -> str:
    path = str(path)
    if len(path) > 1 and path[1] == ":":
        path = f"/{path[0]}{path[2:]}"
    return path.replace("\\", "/")
