from talon import Module, Context, actions


mod = Module()
ctx = Context()

mod.apps.spotify = r"""
os: windows
and app.exe: spotify.exe
"""

ctx.matches = r"""
app: spotify
"""

ctx.tags = ["user.navigation"]


@ctx.action_class("user")
class UserActions:
    def volume_up():
        actions.key("ctrl-up")

    def volume_down():
        actions.key("ctrl-down")
