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
    def file_manager_open_directory(path: str):
        if path.startswith("shell:"):
            actions.insert("start " + path)
            actions.key("enter")
            return
        if path[1] == ":":
            path = f"/{path[0]}{path[2:]}"
        path = path.replace("\\", "/")
        actions.next(path)
