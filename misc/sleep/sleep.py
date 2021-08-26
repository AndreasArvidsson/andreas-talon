from talon import Module, actions, app, noise
import time

mod = Module()

time_last_pop = 0

def on_pop(active: bool):
    global time_last_pop
    if not actions.speech.enabled():
        delta = time.time() - time_last_pop
        if delta >= 0.1 and delta <= 0.3:
            actions.user.talon_wake()
        time_last_pop = time.time()

noise.register("pop", on_pop)


@mod.action_class
class Actions:
    def talon_wake():
        """Wake talon from sleep"""
        actions.speech.enable()
        actions.user.mouse_wake()
        app.notify("Awake")
