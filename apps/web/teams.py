from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.teams = """
tag: browser
and title: /Microsoft Teams/
"""
mod.apps.teams = """
os: windows
and app.exe: Teams.exe
"""

ctx.matches = """
app: teams
"""

ctx.tags = ["user.av"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("ctrl-shift-m")
