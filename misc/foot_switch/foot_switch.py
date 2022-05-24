import time
from talon import Module, Context, actions

mod = Module()
mod.tag("av")

pressed = [False, False, False, False]
timestamps = [0, 0, 0, 0]
scroll_reversed = False
hold_timeout = 0.2


@mod.action_class
class Actions:
    def foot_switch_key(key: int):
        """Press foot switch key. Top(0), Center(1), Left(2), Right(3)"""
        global pressed
        is_pressed = not pressed[key]
        is_held = time.perf_counter() - timestamps[key] > hold_timeout
        pressed = [False, False, False, False]
        pressed[key] = is_pressed
        timestamps[key] = time.perf_counter()

        # Initial downpress
        if is_pressed:
            call_down(key)
        # Button was held and is now released
        elif is_held:
            call_up(key)

    def foot_switch_scroll_reverse():
        """Reverse scroll direction using foot switch"""
        global scroll_reversed
        scroll_reversed = not scroll_reversed

    def foot_switch_top_down():
        """Foot switch button top:down"""
        if scroll_reversed:
            actions.user.mouse_scrolling("down")
        else:
            actions.user.mouse_scrolling("up")

    def foot_switch_top_up():
        """Foot switch button top:up"""
        actions.user.mouse_stop()

    def foot_switch_center_down():
        """Foot switch button center:down"""
        if scroll_reversed:
            actions.user.mouse_scrolling("up")
        else:
            actions.user.mouse_scrolling("down")

    def foot_switch_center_up():
        """Foot switch button center:up"""
        actions.user.mouse_stop()

    def foot_switch_left_down():
        """Foot switch button left:down"""
        actions.user.go_back()

    def foot_switch_left_up():
        """Foot switch button left:up"""
        return ""

    def foot_switch_right_down():
        """Foot switch button right:down"""
        actions.core.repeat_command(1)

    def foot_switch_right_up():
        """Foot switch button right:up"""
        return ""


# Audio / Video conferencing
ctx_av = Context()
ctx_av.matches = r"""
tag: user.av
"""


@ctx_av.action_class("user")
class AvActions:
    def foot_switch_right_down():
        actions.user.mute_microphone()

    def foot_switch_right_up():
        actions.user.mute_microphone()


# Mouse zoom mode
ctx_zoom = Context()
ctx_zoom.matches = r"""
tag: user.zoom_mouse
"""


@ctx_zoom.action_class("user")
class ZoomActions:
    def foot_switch_top_down():
        actions.user.zoom_mouse_click("triple")

    def foot_switch_center_down():
        actions.user.zoom_mouse_click("middle")

    def foot_switch_left_down():
        actions.user.zoom_mouse_click("double")

    def foot_switch_right_down():
        actions.user.zoom_mouse_click("right")

    def foot_switch_top_up():
        pass

    def foot_switch_center_up():
        pass

    def foot_switch_left_up():
        pass

    def foot_switch_right_up():
        pass


def call_down(key: int):
    # Top
    if key == 0:
        actions.user.foot_switch_top_down()
    # Center
    elif key == 1:
        actions.user.foot_switch_center_down()
    # Left
    elif key == 2:
        actions.user.foot_switch_left_down()
    # Right
    elif key == 3:
        actions.user.foot_switch_right_down()


def call_up(key: int):
    # Top
    if key == 0:
        actions.user.foot_switch_top_up()
    # Center
    elif key == 1:
        actions.user.foot_switch_center_up()
    # Left
    elif key == 2:
        actions.user.foot_switch_left_up()
    # Right
    elif key == 3:
        actions.user.foot_switch_right_up()
