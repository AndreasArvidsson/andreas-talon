from talon import noise, actions, cron

cron_job = None
running = False


def on_hiss(active: bool):
    global cron_job
    if not actions.speech.enabled():
        return
    if active:
        if cron_job is None:
            cron_job = cron.after("60ms", hiss_start)
    elif cron_job is not None:
        cron.cancel(cron_job)
        cron_job = None
        if running:
            hiss_stop()


def hiss_start():
    global running
    actions.user.debug("hiss")
    actions.user.mouse_scrolling("down")
    running = True


def hiss_stop():
    global running
    actions.user.debug("hiss:stop")
    actions.user.mouse_stop()
    running = False


noise.register("hiss", on_hiss)
