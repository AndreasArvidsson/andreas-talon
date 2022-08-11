from talon import Module, cron, ctrl

mod = Module()

count_left = 0
pos = (0, 0)
cron_job = None


@mod.action_class
class Actions:
    def stabilized_click():
        """Mouse left click with stabilized cursor position"""
        global pos, count_left, cron_job
        ctrl.mouse_click(button=0)
        count_left += 8
        if cron_job is None:
            pos = ctrl.mouse_pos()
            cron_job = cron.interval("16ms", stabilize_cursor)


def stabilize_cursor():
    global cron_job, count_left
    ctrl.mouse_move(*pos)
    count_left -= 1
    if count_left == 0:
        cron.cancel(cron_job)
        cron_job = None
