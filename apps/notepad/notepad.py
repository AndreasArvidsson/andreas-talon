from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.notepad = r"""
os: windows
and app.exe: notepad.exe
"""

ctx.matches = r"""
app: notepad
"""


@ctx.action_class("win")
class win_actions:
    def filename():
        filename = actions.win.title().split(" - ")[0]
        if "." in filename:
            return filename
        return ""
