from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.openai = """
tag: browser
browser.host: chat.openai.com
"""

ctx.matches = r"""
app: openai
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home shift-enter up")

    def line_insert_down():
        actions.key("end shift-enter")
