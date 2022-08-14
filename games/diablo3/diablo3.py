from talon import Module, Context, actions, cron
import time

mod = Module()
ctx = Context()

mod.apps.diablo3 = """
os: windows
and app.exe: Diablo III64.exe
"""

mod.mode("diablo3", "Used for playing diablo 3")

ctx.matches = r"""
mode: user.diablo3
"""

attack_stand = False
attack_continuous = False

timestamps = {}


def primary_attack():
    """Primary attack in diablo"""
    if attack_stand:
        actions.key("shift:down")

    if attack_continuous:
        actions.mouse_drag(0)
    else:
        actions.mouse_click(0)

    if attack_stand:
        actions.key("shift:up")


@mod.action_class
class Actions:
    def diablo_primary_attack():
        """Primary attack in diablo"""
        global attack_continuous
        attack_continuous = False
        primary_attack()


@ctx.action_class("user")
class UserActions:

    # def noise_hiss_start():
    #     # print("noise_hiss_start")
    #     # global attack_continuous
    #     # attack_continuous = True
    #     # primary_attack()
    #     pass

    # def noise_hiss_stop():
    #     # print("noise_hiss_stop")
    #     pass

    def foot_switch_top_down():
        print("Top down")

    def foot_switch_top_up():
        print("top up")

    def foot_switch_center_down():
        print("center down")
        global attack_stand
        attack_stand = True

    def foot_switch_center_up():
        print("Center up")
        global attack_stand
        attack_stand = False

    def foot_switch_left_down():
        print("left down")

    def foot_switch_left_up():
        print("left up")

    def foot_switch_right_down():
        print("right down")

    def foot_switch_right_up():
        print("Right up")
