from talon import Context, actions, Module

ctx = Context()
mod = Module()

mod.apps.skype = """
os: windows
and app.name: Skype
os: windows
and app.exe: Skype.exe
"""

ctx.matches = r"""
app: skype
"""

ctx.tags = ["user.voip"]


@ctx.action_class("edit")
class EditActions:
    def line_insert_up():
        actions.key("home ctrl-enter up")

    def line_insert_down():
        actions.key("end ctrl-enter")


@ctx.action_class("user")
class UserActions:
    def mute_microphone():
        actions.key("ctrl-m")
