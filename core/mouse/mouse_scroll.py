from talon import Module, actions, app, ui, cron
import time

mod = Module()

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


@mod.action_class
class Actions:
    def mouse_scroll_stop():
        """Stop mouse scroll"""
        global scroll_job, gaze_job
        return_value = scroll_job or gaze_job
        if scroll_job:
            cron.cancel(scroll_job)
            scroll_job = None
        if gaze_job:
            cron.cancel(gaze_job)
            gaze_job = None
        return return_value

    def mouse_scroll_stop_for_click():
        """Stop mouse scroll and wait"""
        if actions.user.mouse_scroll_stop():
            # Make sure scrolling has stopped so that click doesn't miss
            actions.sleep("50ms")

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
                actions.user.mouse_scroll_stop()
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
        actions.user.mouse_scroll_stop()
        _, gaze_origin_y = actions.user.mouse_pos()
        gaze_job = cron.interval("16ms", scroll_gaze_helper)


def scroll_continuous_helper():
    acceleration_speed = 1 + min((time.perf_counter() - scroll_ts) / 0.5, 4)
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


def get_window_for_cursor(x: float, y: float):
    # on windows, check the active_window first since ui.windows() is not z-ordered
    if app.platform == "windows" and ui.active_window().rect.contains(x, y):
        return ui.active_window()

    for window in ui.windows():
        if window.rect.contains(x, y):
            return window

    return None
