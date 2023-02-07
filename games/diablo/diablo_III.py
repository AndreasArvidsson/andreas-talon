from talon import Module, Context, actions, cron
import time

mod = Module()
ctx = Context()

mod.apps.diablo_III = """
os: windows
and app.exe: Diablo III64.exe
"""

mod.mode("diablo_III", "Used for playing diablo 3")

ctx.matches = r"""
mode: user.diablo_III
"""

mod.list("key_diablo3", desc="Diablo 3 keybindings")
ctx.lists["self.key_diablo3"] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "potion": "space",
    "town portal": "t",
    "move": "w",
    "banner": "g",
    "inventory": "i",
    "skills": "s",
    "quests": "q",
    "journal": "j",
    "follower": "f",
    "map": "tab",
    "world": "m",
    "zoom": "z",
    "paragon": "p",
}

attack_stand = False
attack_continuous = False

timestamps = {}


def attack(key: int):
    """Primary attack in diablo"""
    if attack_stand:
        actions.key("shift:down")

    if attack_continuous:
        actions.mouse_drag(key)
    else:
        actions.mouse_click(key)

    if attack_stand:
        actions.key("shift:up")


@ctx.action_class("user")
class UserActions:
    def noise_pop():
        global attack_continuous
        attack_continuous = False
        actions.mouse_release(1)
        attack(0)

    def noise_cluck():
        global attack_continuous
        attack_continuous = False
        actions.mouse_release(0)
        attack(1)

    def noise_hiss_start():
        global attack_continuous
        attack_continuous = True
        attack(0)

    # def noise_hiss_stop():
    #     actions.user.mouse_stop()

    def noise_shush_start():
        global attack_continuous
        attack_continuous = True
        attack(1)

    # def noise_shush_stop():
    #     actions.user.mouse_stop()

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
