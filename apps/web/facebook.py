from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.facebook = """
tag: browser
browser.host: www.facebook.com
"""

ctx.matches = """
app: facebook
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home")
        actions.sleep("10ms")
        actions.key("ctrl-enter up")

    def line_insert_down():
        actions.key("end")
        actions.sleep("10ms")
        actions.key("ctrl-enter")
