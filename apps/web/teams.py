from talon import Context, Module, actions

ctx = Context()
mod = Module()

# Teams meeting
ctx.matches = """
os: windows
app.name: Microsoft Edge
title: /Microsoft Teams/
"""

ctx.tags = ["user.av"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("ctrl-shift-m")
