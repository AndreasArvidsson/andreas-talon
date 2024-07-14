from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.chatgpt = r"""
tag: browser
browser.host: chatgpt.com
"""

ctx.matches = r"""
app: chatgpt
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home")
        actions.key("shift-enter up")

    def line_insert_down():
        actions.key("end")
        actions.key("shift-enter")
