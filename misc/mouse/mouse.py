from talon import Context, Module, actions, app, cron, ctrl, ui, storage
from talon_plugins import eye_mouse
import time

mod = Module()
ctx = Context()

mod.list("mouse_click", desc="Available mouse clicks")
ctx.lists["self.mouse_click"] = {
    "left": "left",
    "right": "right",
    "middle": "middle",
    "mid": "middle",
    "double": "double",
    "dub": "double",
    "triple": "triple",
    "trip": "triple",
    "control": "control",
    "troll": "control",
    "shift": "shift",
    "center": "center",
}

setting_scroll_speed = mod.setting(
    "scroll_speed",
    type=float,
    default=1,
    desc="Base scroll speed",
)
setting_scroll_speed_multiplier = mod.setting(
    "scroll_speed_multiplier",
    type=float,
    default=1,
    desc="Context specific scroll speed multiplier",
)

gaze_job = None
gaze_origin_y = None
scroll_job = None
scroll_speed_dynamic = 1
scroll_dir = 1
scroll_ts = None


@ctx.action_class("main")
class MainActions:
    def mouse_click(button: int = 0):
        ctrl.mouse_click(button=button, hold=16000)


@mod.action_class
class Actions:
    def mouse_on_pop():
        """Mouse on pop handler"""
        stop_scroll_for_click()
        # Left mouse button is held down: end drag
        if 0 in ctrl.mouse_buttons_down():
            actions.user.mouse_drag()
        # Normal click when using control mouse
        elif actions.tracking.control_enabled():
            actions.user.stabilized_click()

    def mouse_click(action: str):
        """Click mouse button"""
        stop_scroll_for_click()
        if action == "left":
            actions.mouse_click()
        elif action == "right":
            actions.mouse_click(1)
        elif action == "middle":
            actions.mouse_click(2)
        elif action == "double":
            actions.mouse_click()
            actions.mouse_click()
        elif action == "triple":
            actions.mouse_click()
            actions.mouse_click()
            actions.mouse_click()
        elif action == "control":
            actions.key("ctrl:down")
            actions.mouse_click()
            actions.key("ctrl:up")
        elif action == "shift":
            actions.key("shift:down")
            actions.mouse_click()
            actions.key("shift:up")
        elif action == "center":
            actions.user.mouse_center_window()
            actions.mouse_click()

    def mouse_pos() -> tuple[float, float]:
        """Mouse position (X, Y)"""
        return ctrl.mouse_pos()

    def mouse_stop():
        """Stops mouse action"""
        # Stop scroll
        if stop_scroll():
            return True
        return False

    def mouse_drag():
        """Press and hold/release button 0 depending on state for dragging"""
        if 0 in ctrl.mouse_buttons_down():
            actions.mouse_release()
            actions.user.notify("Mouse drag: False")
        else:
            actions.mouse_drag()
            actions.user.notify("Mouse drag: True")

    def mouse_scroll(direction: str, times: int):
        """Scrolls"""
        y = times
        if direction == "up":
            y = -y
        actions.mouse_scroll(y, by_lines=True)

    def mouse_scrolling(direction: str):
        """Toggle scrolling continuously"""
        global scroll_job, scroll_dir, scroll_ts
        new_scroll_dir = -1 if direction == "up" else 1

        if scroll_job != None:
            # Issuing a scroll in the same direction as existing aborts it
            if scroll_dir == new_scroll_dir:
                stop_scroll()
                return
            # Issuing a scroll in the reverse direction resets acceleration
            else:
                scroll_dir = new_scroll_dir
                scroll_ts = time.perf_counter()

        if scroll_job is None:
            scroll_dir = new_scroll_dir
            scroll_ts = time.perf_counter()
            scroll_continuous_helper()
            scroll_job = cron.interval("16ms", scroll_continuous_helper)

    def mouse_scroll_speed_set(speed: int):
        """Set scroll speed"""
        global scroll_speed_dynamic
        scroll_speed_dynamic = speed / 10
        actions.user.mouse_scroll_speed_notify()

    def mouse_scroll_speed_increase():
        """Increase scroll speed"""
        global scroll_speed_dynamic
        scroll_speed_dynamic += 0.2
        actions.user.mouse_scroll_speed_notify()

    def mouse_scroll_speed_decrease():
        """Decrease scroll speed"""
        global scroll_speed_dynamic
        scroll_speed_dynamic -= 0.2
        actions.user.mouse_scroll_speed_notify()

    def mouse_scroll_speed_notify():
        """Notify scroll speed"""
        actions.user.notify(f"Mouse scroll speed: {int(scroll_speed_dynamic*100)}%")

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global gaze_job, gaze_origin_y
        stop_scroll()
        _, gaze_origin_y = actions.user.mouse_pos()
        gaze_job = cron.interval("16ms", scroll_gaze_helper)

    def mouse_control_enable():
        """Enable control mouse"""
        mouse_control(eye_mouse.tracker is not None)

    def mouse_control_disable():
        """Disable control mouse"""
        mouse_control(False)

    def mouse_wake():
        """Set control mouse to earlier state"""
        tracking_control = storage.get("tracking_control", False)
        actions.tracking.control_toggle(tracking_control)

    def mouse_sleep():
        """Disables control mouse and scroll"""
        stop_scroll()
        actions.tracking.control_toggle(False)
        # Release all held buttons
        for button in ctrl.mouse_buttons_down():
            actions.mouse_release(button)

    def mouse_sleep_toggle():
        """Toggle sleep/wake for the eye tracker"""
        if actions.tracking.control_enabled():
            actions.user.mouse_sleep()
        else:
            actions.user.mouse_wake()

    def mouse_center_window():
        """Move the mouse cursor to the center of the currently active window"""
        rect = ui.active_window().rect
        actions.mouse_move(rect.center.x, rect.center.y)


def mouse_control(enable: bool):
    storage.set("tracking_control", enable)
    actions.tracking.control_toggle(enable)
    actions.user.notify(f"Control mouse: {enable}")


def stop_scroll():
    global scroll_job, gaze_job
    return_value = scroll_job or gaze_job
    if scroll_job:
        cron.cancel(scroll_job)
        scroll_job = None
    if gaze_job:
        cron.cancel(gaze_job)
        gaze_job = None
    return return_value


def stop_scroll_for_click():
    if stop_scroll():
        # Make sure scrolling has stopped so that click doesn't miss
        actions.sleep("50ms")


def scroll_continuous_helper():
    acceleration_speed = 1 + min((time.perf_counter() - scroll_ts) / 0.5, 3)
    y = (
        setting_scroll_speed.get()
        * setting_scroll_speed_multiplier.get()
        * scroll_speed_dynamic
        * acceleration_speed
        * scroll_dir
    )
    actions.mouse_scroll(y, by_lines=True)


def scroll_gaze_helper():
    x, y = actions.user.mouse_pos()
    window = get_window_for_cursor(x, y)
    if window is None:
        return
    rect = window.rect
    y = ((y - gaze_origin_y) / (rect.height / 3)) ** 3
    actions.mouse_scroll(y, by_lines=True)


def get_screen_for_cursor(x: float, y: float):
    for screen in ui.screens():
        if screen.rect.contains(x, y):
            return screen
    return None


def get_window_for_cursor(x: float, y: float):
    # on windows, check the active_window first since ui.windows() is not z-ordered
    if app.platform == "windows" and ui.active_window().rect.contains(x, y):
        return ui.active_window()

    for window in ui.windows():
        if window.rect.contains(x, y):
            return window

    return None


app.register("launch", lambda: actions.user.mouse_wake())
