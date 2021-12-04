from talon import Module, Context, actions


mod = Module()
ctx = Context()

mod.apps.discord = """
os: windows
and app.name: Discord
os: windows
and app.exe: Discord.exe
"""

ctx.matches = r"""
app: discord
"""


@ctx.action_class("edit")
class EditActions:
    def delete_word():
        actions.edit.select_word()
        actions.sleep("100ms")
        actions.edit.delete()

    def line_insert_up():
        actions.key("home shift-enter up")

    def line_insert_down():
        actions.key("end shift-enter")


@ctx.action_class("user")
class UserActions:
    def delete_word_right():
        actions.user.select_word_right()
        actions.sleep("100ms")
        actions.edit.delete()

    def mute_microphone():
        actions.key("ctrl-shift-m")
