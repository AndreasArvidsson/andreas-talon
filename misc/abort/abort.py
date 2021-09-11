from talon import actions, speech_system


def on_phrase(d):
    if not actions.speech.enabled():
        return
    try:
        words = d["parsed"]._unmapped
        if words[-1] == "cancel":
            d["parsed"]._sequence = []
    except:
        pass


speech_system.register("pre:phrase", on_phrase)
