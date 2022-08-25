from talon import Module, Context, actions, noise, cron

mod = Module()
ctx = Context()

ctx.matches = r"""
mode: command
"""

cron_job = None
running = False


@ctx.action_class("user")
class UserActions:
    def noise_hiss_start():
        actions.user.mouse_scrolling("down")

    def noise_hiss_stop():
        actions.user.mouse_stop()


@mod.action_class
class Actions:
    def noise_hiss_start():
        """Noise hiss started"""

    def noise_hiss_stop():
        """Noise hiss stopped"""


def on_hiss(active: bool):
    global cron_job, running
    if not actions.speech.enabled():
        return
    if active:
        if cron_job is None:
            cron_job = cron.after("70ms", hiss_start)
    elif cron_job is not None:
        cron.cancel(cron_job)
        cron_job = None
        if running:
            running = True
            hiss_stop()


def hiss_start():
    global running
    running = True
    actions.user.debug("hiss")
    actions.user.noise_hiss_start()


def hiss_stop():
    global running
    running = False
    actions.user.debug("hiss:stop")
    actions.user.noise_hiss_stop()


# noise.register("hiss", on_hiss)
