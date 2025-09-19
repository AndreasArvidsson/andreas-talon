from talon import Module, Context, actions


mod = Module()
mod.tag("codex")

ctx = Context()
ctx.matches = r"""
app: codex-cli
"""


@ctx.action_class("edit")
class Actions:
    def line_insert_down():
        actions.key("ctrl-j")
