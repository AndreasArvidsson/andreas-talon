import time
from talon import Module, Context, actions

mod = Module()
mod.tag("av")

pressed = [False, False, False, False]
timestamps = [0, 0, 0, 0]
scroll_reversed = False


@mod.action_class
class Actions:
    def foot_switch_key(key: int) -> bool:
        """Press foot switch key. Top(0), Center(1), Left(2), Right(3)"""
        is_down = not pressed[key]
        pressed[key] = is_down

        if is_down:
            timestamps[key] = time.perf_counter()
        else:
            is_hold = time.perf_counter() - timestamps[key] > 0.5

        # Top
        if key == 0:
            if is_down:
                actions.user.foot_switch_top_down()
            elif is_hold:
                actions.user.foot_switch_top_up()
        # Center
        elif key == 1:
            if is_down:
                actions.user.foot_switch_center_down()
            elif is_hold:
                actions.user.foot_switch_center_up()
        # Left
        elif key == 2:
            if is_down:
                actions.user.foot_switch_left_down()
            elif is_hold:
                actions.user.foot_switch_left_up()
        # Right
        elif key == 3:
            if is_down:
                actions.user.foot_switch_right_down()
            elif is_hold:
                actions.user.foot_switch_right_up()

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
        actions.user.mute()

    def foot_switch_right_up():
        actions.user.mute()


# Mouse zoom mode
ctx_zoom = Context()
ctx_zoom.matches = r"""
mode: user.zoom_mouse
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
        return ""

    def foot_switch_center_up():
        return ""

    def foot_switch_left_up():
        return ""

    def foot_switch_right_up():
        return ""
