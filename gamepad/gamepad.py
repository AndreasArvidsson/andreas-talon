from talon import Module, actions, cron

mod = Module()
multiplier = 3
cron_job = None
_x = 0
_y = 0


@mod.action_class
class Actions:
    def gamepad_scroll(x: float, y: float):
        """Perform gamepad scrolling"""
        global cron_job, _x, _y
        _x = x * multiplier
        _y = y * -1 * multiplier

        if _x != 0 or _y != 0:
            if cron_job is None:
                cron_job = cron.interval("16ms", scroll_continuous_helper)
        elif cron_job is not None:
            cron.cancel(cron_job)
            cron_job = None


def scroll_continuous_helper():
    actions.mouse_scroll(x=_x, y=_y, by_lines=True)
