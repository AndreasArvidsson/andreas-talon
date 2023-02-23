from talon import Context, Module, actions

ctx = Context()
mod = Module()

mod.apps.talon_speech = """
tag: browser
title: /Talon Speech Collection/
"""

ctx.matches = """
app: talon_speech
"""


@ctx.action_class("edit")
class EditActions:
    def left():
        actions.skip()

    def right():
        actions.skip()


@ctx.action_class("user")
class UserActions:
    def foot_switch_left_down():
        down()

    def foot_switch_right_down():
        down()

    def foot_switch_left_up():
        up()

    def foot_switch_right_up():
        up()


def down():
    actions.key("space")


def up():
    actions.key("space")
    actions.sleep("300ms")
    actions.key("down")
