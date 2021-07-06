from talon import Module, Context, actions
key = actions.key

mod = Module()
ctx = Context()

mod.apps.foobar = """
os: windows
and app.name: foobar2000
os: windows
and app.exe: foobar2000.exe
"""

ctx.matches = r"""
app: foobar
"""

ctx.tags = ["user.tabs"]


@ctx.action_class("user")
class UserActions:
    def volume_up():    key("ctrl-up")
    def volume_down():  key("ctrl-down")
