from talon import actions, speech_system
from talon import Module, app


mod = Module()


def on_phrase(d):
    if not actions.speech.enabled():
        return
    try:
        words = d["parsed"]._unmapped
    except:
        return
    if words[-1] == "cancel":
        d["parsed"]._sequence = []
        text = " ".join(words[:-1])
        if text:
            app.notify(f"Aborted command:\n{text}")


speech_system.register("pre:phrase", on_phrase)
