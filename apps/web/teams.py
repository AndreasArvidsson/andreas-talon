from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.teams = """
tag: browser
browser.host: teams.microsoft.com
"""
mod.apps.teams = """
os: windows
and app.exe: Teams.exe
"""

ctx.matches = """
app: teams
"""

ctx.tags = ["user.voip"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("ctrl-shift-m")
