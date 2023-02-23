from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.facebook = """
tag: browser
title: /Facebook/
"""

ctx.matches = """
app: facebook
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home ctrl-enter up")

    def line_insert_down():
        actions.key("end ctrl-enter")
