from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.robomongo = """
os: windows
and app.name: Robo 3T, MongoDB management tool
os: windows
and app.exe: robo3t.exe
"""

ctx.matches = r"""
app: robomongo
"""

ctx.tags = ["user.comments", "user.tabs", "user.find"]


@ctx.action_class("app")
class AppActions:
    def tab_reopen():
        actions.skip()


@ctx.action_class("edit")
class EditActions:
    def find(text: str = None):
        actions.key("ctrl-f")
        if text:
            actions.sleep("50ms")
            actions.insert(text)


@ctx.action_class("user")
class UserActions:
    def tab_duplicate():
        actions.key("ctrl-shift-t")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("ctrl-shift-c")
