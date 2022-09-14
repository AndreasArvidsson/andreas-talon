from talon import Module, Context, actions

mod = Module()

mod.apps.kodi = """
os: windows
and app.exe: kodi.exe
"""

ctx = Context()

ctx.matches = r"""
app: kodi
"""


@ctx.action_class("user")
class UserActions:
    def go_back():
        actions.key("backspace")
