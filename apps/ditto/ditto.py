from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.ditto = """
os: windows
and app.name: Ditto
os: windows
and app.exe: Ditto.exe
"""

ctx.matches = "app: ditto"


@ctx.action_class("edit")
class EditActions:
    def paste():
        actions.key("enter")

    def paste_match_style():
        actions.key("shift-enter")
