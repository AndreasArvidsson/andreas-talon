from talon import Module, cron, actions

mod = Module()
cron_job = None


@mod.action_class
class Actions:
    def stabilized_click():
        """Mouse left click with stabilized cursor position"""
        global cron_job
        actions.user.mouse_freeze_toggle(True)
        cron.cancel(cron_job)
        cron_job = cron.after("128ms", unfreeze_cursor)
        actions.mouse_click()


def unfreeze_cursor():
    global cron_job
    cron_job = None
    actions.user.mouse_freeze_toggle(False)
