from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.jitsi = """
tag: browser
and title: /\\| Jitsi Meet/
"""

ctx.matches = r"""
app: jitsi
"""

ctx.tags = ["user.av"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("m")
