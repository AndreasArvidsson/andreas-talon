from talon import Module, Context, actions
key = actions.key
insert = actions.insert
ctx = Context()
mod = Module()


mod.apps.windows_terminal = """
os: windows
and app.name: WindowsTerminal.exe
os: windows
and app.exe: WindowsTerminal.exe
"""

ctx.matches = r"""
app: windows_terminal
"""


@ctx.action_class("app")
class AppActions:
    def tab_previous():         key("ctrl-shift-tab")
    def tab_next():             key("ctrl-tab")
    def preferences():          key("ctrl-,")

@ctx.action_class("edit")
class EditActions:
    def copy():                 key("ctrl-shift-c")
    def paste():                key("ctrl-shift-v")


@ctx.action_class("user")
class UserActions:
    def tab_duplicate():        key("ctrl-d")
