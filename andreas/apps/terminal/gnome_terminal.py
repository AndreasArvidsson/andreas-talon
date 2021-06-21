from talon import Module, Context, actions
key = actions.key
insert = actions.insert
user = actions.user

mod = Module()

mod.apps.gnome_terminal = """
os: linux
and app.name: Gnome-terminal
"""

ctx = Context()
ctx.matches = """
app: gnome_terminal
"""

ctx.tags = ["terminal", "user.bash", "user.tabs"]

@ctx.action_class("app")
class AppActions:
    def window_open():      key("ctrl-shift-n")
    def tab_open():         key("ctrl-shift-t")
    def tab_close():        key("ctrl-shift-w")

@ctx.action_class("edit")
class EditActions:
    def copy():             key("ctrl-shift-c")
    def paste():            key("ctrl-shift-v")


@ctx.action_class("user")
class UserActions:
    def tab_jump(number: int):
        key(f"alt-{number}")
