from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.zoom = """
os: windows
and app.name: Zoom Meetings
os: windows
and app.exe: Zoom.exe
"""

ctx.matches = r"""
app: zoom
"""

ctx.tags = ["user.voip"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("alt-a")
