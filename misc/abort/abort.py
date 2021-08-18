from talon import actions, speech_system
from talon import Module, app


mod = Module()


def fn(d):
    try:
        words = d["parsed"]._unmapped
    except:
        return
    if words[-1] == "cancel" and actions.speech.enabled():
        d["parsed"]._sequence = []
        text = " ".join(words[:-1])
        if len(text):
            app.notify(f"Aborted command:\n{text}")


speech_system.register("pre:phrase", fn)
