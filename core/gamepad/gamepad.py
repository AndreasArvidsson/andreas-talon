from talon import Module, actions, cron

mod = Module()
cron_job = None
slow_mode = False
_x = 0
_y = 0

@mod.action_class
class Actions:
    def gamepad_scroll(x: float, y: float):
        """Perform gamepad scrolling"""
        global cron_job, _x, _y
        if slow_mode:
            _x = x * 1.5
            _y = y * 1.5
        else:
            _x = x * 3
            _y = y * 3

        if _x != 0 or _y != 0:
            if cron_job is None:
                cron_job = cron.interval("16ms", scroll_continuous_helper)
        elif cron_job is not None:
            cron.cancel(cron_job)
            cron_job = None

    def gamepad_scroll_slow_toggle():
        """Toggle gamepad scroll slow mode"""
        global slow_mode
        slow_mode = not slow_mode
        actions.user.notify(f"Gamepad slow scroll: {slow_mode}")


def scroll_continuous_helper():
    actions.mouse_scroll(x=_x, y=_y, by_lines=True)
