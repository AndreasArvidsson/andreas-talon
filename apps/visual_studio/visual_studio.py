from talon import Module, Context, actions, ui

mod = Module()


mod.apps.visual_studio = r"""
os: windows
app.name: Microsoft Visual Studio 2022
"""

ctx = Context()
ctx.matches = r"""
app: visual_studio
"""


@ctx.action_class("code")
class LangCodeActions:
    def language() -> str:
        return "cplusplus"


@ctx.action_class("app")
class AppActions:
    def tab_close():
        actions.key("ctrl-f4")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_reopen():
        actions.key("ctrl-1 ctrl-r enter")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("ctrl-k ctrl-'")

    def complete():
        actions.key("ctrl-space")
        actions.app.window_close


@ctx.action_class("user")
class UserActions:
    # ----- Navigation -----
    def go_back():
        actions.key("ctrl--")

    def go_forward():
        actions.key("ctrl-shift--")


@mod.action_class
class Actions:
    def format_document():
        """Format document"""
        actions.key("ctrl-k ctrl-d")
