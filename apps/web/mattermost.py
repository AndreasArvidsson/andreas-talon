from talon import Context, actions, Module, app

ctx = Context()
mod = Module()

mod.apps.mattermost = """
tag: browser
and title: /Mattermost/
"""

ctx.matches = r"""
app: mattermost
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home shift-enter up")

    def line_insert_down():
        actions.key("end shift-enter")
