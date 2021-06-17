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

@ctx.action_class("user")
class UserActions:
    def file_manager_open_directory(path: str):
        if path.startswith("shell:"):
            actions.user.exec(path)
            return
        if path[1] == ":":
            path = f"/mnt/{path[0].lower()}{path[2:]}"
        path = path.replace("\\", "/")
        actions.next(path)
