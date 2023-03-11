from talon import Module, Context, cron, actions

mod = Module()

state = {}
cron_jobs = {}
callbacks = {}

ctx = Context()
ctx.matches = r"""
mode: command
mode: dictation
"""


@ctx.action_class("user")
class UserActions:
    def noise_pop():
        actions.user.mouse_on_pop()

    def noise_cluck():
        actions.core.repeat_phrase()

    def noise_shush_start():
        actions.user.mouse_scrolling("up")

    def noise_shush_stop():
        actions.user.mouse_scroll_stop()

    def noise_hiss_start():
        actions.user.mouse_scrolling("down")

    def noise_hiss_stop():
        actions.user.mouse_scroll_stop()


@mod.action_class
class Actions:
    def noise_debounce(name: str, active: bool):
        """Start or stop continuous noise using debounce"""
        if name not in state:
            state[name] = active
            cron_jobs[name] = cron.after("80ms", lambda: callback(name))
        elif state[name] != active:
            cron.cancel(cron_jobs[name])
            state.pop(name)

    def noise_pop():
        """Noise pop"""

    def noise_cluck():
        """Noise cluck"""

    def noise_shush_start():
        """Noise shush started"""

    def noise_shush_stop():
        """Noise shush stopped"""

    def noise_hiss_start():
        """Noise hiss started"""

    def noise_hiss_stop():
        """Noise hiss stopped"""


def callback(name: str):
    active = state.pop(name)
    callbacks[name](active)


def on_shush(active: bool):
    if active:
        actions.user.debug("shush:start")
        actions.user.noise_shush_start()
    else:
        actions.user.debug("shush:stop")
        actions.user.noise_shush_stop()


def on_hiss(active: bool):
    if active:
        actions.user.debug("hiss:start")
        actions.user.noise_hiss_start()
    else:
        actions.user.debug("hiss:stop")
        actions.user.noise_hiss_stop()


callbacks["shush"] = on_shush
callbacks["hiss"] = on_hiss
