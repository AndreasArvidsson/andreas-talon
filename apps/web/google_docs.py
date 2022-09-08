from talon import Context, actions, Module

ctx = Context()
mod = Module()

ctx.matches = """
tag: browser
title: /Links - Google Docs/
"""


@ctx.action_class("edit")
class EditActions:
    def paste():
        actions.next()
        actions.sleep("300ms")
        actions.edit.line_insert_down()
        actions.edit.line_insert_down()
        actions.user.tab_back()
