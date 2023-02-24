from talon import Context, Module, actions
from talon.clip import MimeData
import json
import re

ctx = Context()
mod = Module()

mod.apps.slack = """
tag: browser
browser.host: app.slack.com
"""

ctx.matches = """
app: slack
"""


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home ctrl-enter up")

    def line_insert_down():
        actions.key("end ctrl-enter")


@mod.action_class
class UserActions:
    def slack_open_search_result(search: str):
        """Opens the given search result on slack"""
        actions.key("ctrl-k")
        actions.insert(search)
        actions.sleep("400ms")
        actions.key("enter")
