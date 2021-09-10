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
class user_actions:
    def line_insert_down():
        actions.key("end shift-enter")
