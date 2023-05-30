from talon import Module, cron, actions

mod = Module()
cron_job = None


@mod.action_class
class Actions:
    def stabilized_click():
        """Mouse left click with stabilized cursor position"""
        global cron_job
        actions.tracking.control_toggle(False)
        cron.cancel(cron_job)
        cron_job = cron.after("150ms", unfreeze_cursor)
        actions.mouse_click()


def unfreeze_cursor():
    global cron_job
    cron_job = None
    actions.tracking.control_toggle(True)
