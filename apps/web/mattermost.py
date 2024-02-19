from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.mattermost = r"""
tag: browser
browser.host: mattermost.redpill-linpro.com
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
