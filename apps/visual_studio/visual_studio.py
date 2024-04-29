from talon import Module, Context, actions

mod = Module()


mod.apps.visual_studio = r"""
os: windows
app.name: Microsoft Visual Studio 2022
"""

ctx = Context()
ctx.matches = r"""
app: visual_studio
"""


@ctx.action_class("app")
class AppActions:
    def tab_close():
        actions.key("ctrl-f4")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("ctrl-k ctrl-'")

    def complete():
        actions.key("ctrl-space")
        actions.app.window_close


@mod.action_class
class Actions:
    def format_document():
        """Format document"""
        actions.key("ctrl-k ctrl-d")
