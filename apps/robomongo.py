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

ctx.tags = ["user.comments", "user.tabs"]


@ctx.action_class("app")
class AppActions:
    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_reopen():
        actions.skip()


@ctx.action_class("user")
class UserActions:
    def tab_duplicate():
        actions.key("ctrl-shift-t")


@ctx.action_class("code")
class CodeActions:
    def toggle_comment():
        actions.key("ctrl-shift-c")
