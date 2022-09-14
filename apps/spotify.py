from talon import Module, Context, actions


mod = Module()
ctx = Context()

mod.apps.spotify = """
os: windows
and app.name: Spotify.exe
os: windows
and app.exe: Spotify.exe
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
