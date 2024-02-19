from talon import Module, Context, actions

ctx = Context()
mod = Module()


mod.apps.windows_terminal = r"""
os: windows
and app.exe: windowsterminal.exe
"""

ctx.matches = r"""
app: windows_terminal
"""


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.key("ctrl-shift-n")

    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_close():
        actions.key("ctrl-shift-w")

    def preferences():
        actions.key("ctrl-,")


@ctx.action_class("edit")
class EditActions:
    def copy():
        actions.key("ctrl-shift-c")

    def paste():
        actions.key("ctrl-shift-v")

    def find(text: str = None):
        actions.key("ctrl-shift-f")
        if text:
            actions.insert(text)


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        if number < 9:
            actions.key(f"ctrl-alt-{number}")

    def tab_final():
        actions.key("ctrl-alt-9")

    def tab_duplicate():
        actions.key("ctrl-shift-d")
