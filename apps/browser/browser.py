from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: browser
"""

browser_name = "Firefox"


@ctx.action_class("browser")
class BrowserActions:
    def go_back():
        actions.key("alt-left")

    def go_forward():
        actions.key("alt-right")


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
        if actions.app.name() != browser_name:
            actions.user.focus_name(browser_name)
            actions.sleep("50ms")
        actions.user.browser_open(url)
