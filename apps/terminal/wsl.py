from talon import Module, Context, actions

key = actions.key
insert = actions.insert
user = actions.user

mod = Module()

mod.apps.wsl = r"""
app: windows_terminal
and win.title: /\w+@\w+: /i
"""
mod.apps.wsl = """
os: windows
and app.name: Microsoft Windows Subsystem for Linux Launcher
os: windows
and app.exe: wsl.exe
"""

ctx = Context()
ctx.matches = """
app: wsl
"""

ctx.tags = ["terminal", "user.bash"]


@ctx.action_class("path")
class PathActions:
    def talon_app():
        return update_path(actions.next())

    def talon_home():
        return update_path(actions.next())

    def talon_user():
        return update_path(actions.next())

    def user_home():
        return update_path(actions.next())


@ctx.action_class("user")
class UserActions:
    def file_manager_open_directory(path: str):
        if path.startswith("shell:"):
            actions.user.exec(path)
            return
        path = update_path(path)
        actions.next(path)


def update_path(path: str):
    path = str(path)
    if path[1] == ":":
        path = f"/mnt/{path[0].lower()}{path[2:]}"
    return path.replace("\\", "/")
