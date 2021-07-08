from talon import Module, Context, actions
key = actions.key

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


@ctx.action_class("user")
class UserActions:
    def volume_up():    key("ctrl-up")
    def volume_down():  key("ctrl-down")
