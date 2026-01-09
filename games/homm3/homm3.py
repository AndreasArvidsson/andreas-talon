from talon import Module, Context, actions

mod = Module()

mod.apps.homm3 = r"""
os: windows
and app.exe: h3hota hd.exe
"""

ctx = Context()
ctx.matches = r"""
app: homm3
"""


@ctx.action_class("user")
class MainActions:
    def foot_switch_top_down():
        actions.user.key_hold("ctrl-up")

    def foot_switch_top_up(held: bool):
        actions.user.key_release("ctrl-up")

    def foot_switch_center_down():
        actions.user.key_hold("ctrl-down")

    def foot_switch_center_up(held: bool):
        actions.user.key_release("ctrl-down")

    def foot_switch_left_down():
        actions.user.key_hold("ctrl-left")

    def foot_switch_left_up(held: bool):
        actions.user.key_release("ctrl-left")

    def foot_switch_right_down():
        actions.user.key_hold("ctrl-right")

    def foot_switch_right_up(held: bool):
        actions.user.key_release("ctrl-right")
