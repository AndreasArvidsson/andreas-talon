import time
from talon import Module, Context, actions, cron

mod = Module()

settings_timeout = mod.setting(
    "foot_switch_timeout",
    type=bool,
    default=True,
    desc="If true timeout will be used to decide if the foot switch was held or not",
)

LEFT = 0
CENTER = 1
RIGHT = 2
TOP = 3

EVENT_NONE = 0
EVENT_DOWN = 1
EVENT_UP = 2

events = [EVENT_NONE, EVENT_NONE, EVENT_NONE, EVENT_NONE]
timestamps = [0, 0, 0, 0]
scroll_reversed = False
hold_timeout = 0.2


def on_interval():
    for key, event in enumerate(events):
        if event == EVENT_NONE:
            continue

        events[key] = EVENT_NONE

        if event == EVENT_DOWN:
            call_down(key)
        # Key is released after specified hold time out. ie key was held.
        elif (
            not settings_timeout.get()
            or time.perf_counter() - timestamps[key] > hold_timeout
        ):
            call_up(key)


# In a hotkey event, eg "key(ctrl:down)", any key you press with key/insert
# actions will be combined with ctrl since it's still held. Just updating a
# boolean in the actual hotkey event and reading it asynchronously with cron
# gets around this issue.
cron.interval("16ms", on_interval)


def call_down(key: int):
    if key == LEFT:
        actions.user.foot_switch_left_down()
    elif key == CENTER:
        actions.user.foot_switch_center_down()
    elif key == RIGHT:
        actions.user.foot_switch_right_down()
    elif key == TOP:
        actions.user.foot_switch_top_down()


def call_up(key: int):
    if key == LEFT:
        actions.user.foot_switch_left_up()
    elif key == CENTER:
        actions.user.foot_switch_center_up()
    elif key == RIGHT:
        actions.user.foot_switch_right_up()
    elif key == TOP:
        actions.user.foot_switch_top_up()


@mod.action_class
class Actions:
    def foot_switch_down(key: int):
        """Foot switch key down event. Left(0), Center(1), Right(2), Top(3)"""
        timestamps[key] = time.perf_counter()
        events[key] = EVENT_DOWN

    def foot_switch_up(key: int):
        """Foot switch key up event. Left(0), Center(1), Right(2), Top(3)"""
        events[key] = EVENT_UP

    def foot_switch_scroll_reverse():
        """Reverse scroll direction using foot switch"""
        global scroll_reversed
        scroll_reversed = not scroll_reversed

    def foot_switch_top_down():
        """Foot switch button top:down"""

    def foot_switch_top_up():
        """Foot switch button top:up"""

    def foot_switch_center_down():
        """Foot switch button center:down"""

    def foot_switch_center_up():
        """Foot switch button center:up"""

    def foot_switch_left_down():
        """Foot switch button left:down"""

    def foot_switch_left_up():
        """Foot switch button left:up"""

    def foot_switch_right_down():
        """Foot switch button right:down"""

    def foot_switch_right_up():
        """Foot switch button right:up"""


# ---------- Default implementation ----------
ctx = Context()


@ctx.action_class("user")
class UserActions:
    def foot_switch_top_down():
        if scroll_reversed:
            actions.user.mouse_scrolling("down")
        else:
            actions.user.mouse_scrolling("up")

    def foot_switch_top_up():
        actions.user.mouse_scroll_stop()

    def foot_switch_center_down():
        if scroll_reversed:
            actions.user.mouse_scrolling("up")
        else:
            actions.user.mouse_scrolling("down")

    def foot_switch_center_up():
        actions.user.mouse_scroll_stop()

    def foot_switch_left_down():
        actions.user.go_back()

    def foot_switch_left_up():
        pass

    def foot_switch_right_down():
        pass

    def foot_switch_right_up():
        pass


# ---------- Default non-sleep implementation ----------
ctx_eye_tracker = Context()
ctx_eye_tracker.matches = r"""
tag: user.eye_tracker
tag: user.eye_tracker_frozen
"""


@ctx_eye_tracker.action_class("user")
class NonSleepActions:
    def foot_switch_right_down():
        actions.user.mouse_freeze_toggle()

    def foot_switch_right_up():
        actions.user.mouse_freeze_toggle()


# ---------- Audio conferencing ----------
ctx_voip = Context()
ctx_voip.matches = r"""
mode: command
mode: dictation
mode: sleep
tag: user.voip
"""


@ctx_voip.action_class("user")
class VoipActions:
    def foot_switch_left_down():
        actions.user.mute_microphone()

    def foot_switch_left_up():
        actions.user.mute_microphone()
