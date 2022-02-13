from talon import noise, actions


def on_pop(active: bool):
    # In command mode
    if actions.speech.enabled():
        actions.user.mouse_on_pop()
    # In sleep mode
    else:
        actions.user.talon_wake_on_pop()


noise.register("pop", on_pop)
