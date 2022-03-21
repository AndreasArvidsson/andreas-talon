from talon import Context, actions, Module

ctx = Context()
mod = Module()

ctx.matches = """
tag: browser
and title: /Links - Google Docs/
"""


@ctx.action_class("edit")
class EditActions:
    def paste():
        actions.next()
        actions.sleep(0.1)
        actions.edit.line_insert_down()
        actions.edit.line_insert_down()
