from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.studio3t = r"""
os: windows
and app.exe: studio 3t community edition.exe
"""

ctx.matches = r"""
app: studio3t
"""

ctx.tags = ["user.code_comments", "user.tabs", "user.find"]


@ctx.action_class("app")
class AppActions:
    def tab_open():
        actions.key("ctrl-l")

    def tab_close():
        actions.key("ctrl-f4")

    def tab_reopen():
        actions.skip()


@ctx.action_class("edit")
class EditActions:
    @staticmethod
    def find(text: str = ""):
        actions.key("ctrl-f")
        if text:
            actions.sleep("50ms")
            actions.insert(text)


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("ctrl-/")
