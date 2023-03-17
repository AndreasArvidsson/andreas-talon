from talon import Module, Context, actions

key = actions.key
insert = actions.insert
user = actions.user

mod = Module()

mod.apps.git_bash = """
app: windows_terminal
and win.title: /MINGW64:/i
"""
mod.apps.git_bash = """
os: windows
and app.name: mintty.exe
os: windows
and app.exe: mintty.exe
"""
mod.apps.git_bash = """
os: windows
app: vscode
win.file_ext: .bashbook
"""

ctx = Context()
ctx.matches = """
app: git_bash
"""

ctx.tags = ["user.bash"]


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
