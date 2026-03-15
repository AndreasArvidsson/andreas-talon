from talon import Module, Context, actions

mod = Module()
mod.tag("codex_cli")

ctx = Context()
ctx.matches = r"""
tag: codex_cli
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
