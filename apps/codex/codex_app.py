from talon import Module, Context, actions


mod = Module()

mod.apps.codex = r"""
os: windows
and app.exe: codex.exe
"""

ctx = Context()
ctx.matches = r"""
app: codex
"""


@ctx.action_class("edit")
class Actions:
    def line_insert_up():
        actions.key("home")
        actions.sleep("10ms")
        actions.key("shift-enter up")

    def line_insert_down():
        actions.key("end")
        actions.sleep("10ms")
        actions.key("shift-enter")
