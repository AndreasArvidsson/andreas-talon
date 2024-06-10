from talon import Module, Context, actions

mod = Module()

mod.apps.gnome_terminal = r"""
os: linux
and app.name: Gnome-terminal
"""

ctx = Context()
ctx.matches = r"""
app: gnome_terminal
"""

ctx.tags = ["terminal", "user.bash", "user.tabs"]


@ctx.action_class("app")
class AppActions:
    def window_open():
        actions.key("ctrl-shift-n")

    def tab_open():
        actions.key("ctrl-shift-t")

    def tab_close():
        actions.key("ctrl-shift-w")


@ctx.action_class("edit")
class EditActions:
    def copy():
        actions.key("ctrl-shift-c")

    def paste():
        actions.key("ctrl-shift-v")
        actions.sleep("30ms")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        actions.key(f"alt-{number}")
