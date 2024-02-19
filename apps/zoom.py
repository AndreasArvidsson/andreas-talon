from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.zoom = r"""
os: windows
and app.exe: zoom.exe
"""

ctx.matches = r"""
app: zoom
"""

ctx.tags = ["user.voip"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("alt-a")
