from talon import Module, actions, speech_system, app

def on_pre_phrase(d):
    words = d["parsed"]._unmapped
    if words[-1] == "cancel" and actions.speech.enabled():
        app.notify("Command aborted: " + " ".join(d["phrase"]))
        d["parsed"]._sequence = []

speech_system.register("pre:phrase", on_pre_phrase)