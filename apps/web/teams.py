from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.teams = r"""
os: windows
and app.exe: teams.exe
os: windows
and app.exe: ms-teams.exe
"""
mod.apps.teams = r"""
tag: browser
browser.host: teams.microsoft.com
"""

ctx.matches = r"""
app: teams
"""

ctx.tags = ["user.voip"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("ctrl-shift-m")
