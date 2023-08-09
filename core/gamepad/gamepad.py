from talon import Module, actions, cron
import time

HOLD_TIMEOUT = 0.2

mod = Module()
cron_job = None
slow_mode = False
mouse_freeze_time = 0
_x = 0
_y = 0


@mod.action_class
class Actions:
    def gamepad_scroll(x: float, y: float):
        """Perform gamepad scrolling"""
        global cron_job, _x, _y
        multiplier = 1.5 if slow_mode else 3
        _x = x * multiplier
        _y = y * multiplier

        if _x != 0 or _y != 0:
            if cron_job is None:
                cron_job = cron.interval("16ms", scroll_continuous_helper)
        elif cron_job is not None:
            cron.cancel(cron_job)
            cron_job = None

    def gamepad_mouse_freeze(button_down: bool):
        """Toggle gamepad mouse freeze"""
        global mouse_freeze_time
        if button_down:
            mouse_freeze_time = time.perf_counter()
            actions.user.mouse_freeze_toggle()
        elif time.perf_counter() - mouse_freeze_time > HOLD_TIMEOUT:
            actions.user.mouse_freeze_toggle()

    def gamepad_scroll_slow_toggle():
        """Toggle gamepad slow scroll mode"""
        global slow_mode
        slow_mode = not slow_mode
        actions.user.notify(f"Gamepad slow scroll: {slow_mode}")


def scroll_continuous_helper():
    actions.mouse_scroll(x=_x, y=_y, by_lines=True)
