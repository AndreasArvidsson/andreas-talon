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

@ctx.action_class("edit")
class EditActions:
    def line_insert_down():
        actions.key("end ctrl-enter")
