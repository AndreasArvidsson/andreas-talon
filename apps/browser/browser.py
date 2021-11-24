from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: browser
"""


@ctx.action_class("user")
class UserActions:
    def go_back():
        actions.browser.go_back()

    def go_forward():
        actions.browser.go_forward()


@mod.action_class
class Actions:
    def browser_open(url: str):
        """Open url in browser"""

    def browser_focus_open(url: str):
        """Focus browser and open url"""
        actions.user.focus_name("Firefox")
        actions.user.browser_open(url)
