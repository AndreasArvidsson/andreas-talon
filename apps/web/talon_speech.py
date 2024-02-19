from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.talon_speech = r"""
tag: browser
browser.host: speech.talonvoice.com
"""

ctx.matches = r"""
mode: sleep
app: talon_speech
"""


@ctx.action_class("user")
class UserActions:
    def foot_switch_top_down():
        actions.key("up")

    def foot_switch_top_up(held: bool):
        pass

    def foot_switch_center_down():
        actions.key("down")

    def foot_switch_center_up(held: bool):
        pass

    def foot_switch_left_down():
        down()

    def foot_switch_left_up(held: bool):
        up()

    def foot_switch_right_down():
        down()

    def foot_switch_right_up(held: bool):
        up()


def down():
    actions.key("space")


def up():
    actions.key("space")
    actions.sleep("350ms")
    actions.key("down")
