from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.jitsi = r"""
tag: browser
browser.host: meet.jit.si
browser.host: meet.redpill-linpro.com
"""

ctx.matches = r"""
app: jitsi
"""

ctx.tags = ["user.voip"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("m")
