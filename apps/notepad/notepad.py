from talon import Context, actions, Module, app

ctx = Context()
mod = Module()

mod.apps.notepad = """
os: windows
and app.name: Notepad
os: windows
and app.exe: notepad.exe
"""

ctx.matches = r"""
app: notepad
"""


@ctx.action_class("win")
class win_actions:
    def filename():
        title = actions.win.title()
        result = title.split(" - ")[0]
        if "." in result:
            return result
        return ""
