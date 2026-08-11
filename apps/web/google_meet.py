from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.google_meet = r"""
tag: browser
browser.host: meet.google.com
"""

ctx.matches = r"""
app: google_meet
"""

ctx.tags = ["user.voip"]


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("ctrl-d")
