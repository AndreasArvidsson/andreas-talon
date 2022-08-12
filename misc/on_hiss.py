from talon import noise, actions, cron

cron_job = None


def on_hiss(active: bool):
    global cron_job
    if not actions.speech.enabled():
        return
    if active:
        if cron_job is None:
            cron_job = cron.after("50ms", hiss_start)
    elif cron_job:
        cron.cancel(cron_job)
        cron_job = None
        hiss_stop()


def hiss_start():
    actions.user.debug("hiss")
    actions.user.mouse_scrolling("down")


def hiss_stop():
    actions.user.debug("hiss:stop")
    actions.user.mouse_stop()


noise.register("hiss", on_hiss)
