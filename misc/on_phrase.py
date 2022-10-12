from talon import Module, speech_system, actions
import time

mod = Module()

ts_threshold = None


@mod.action_class
class Actions:
    def abort_current_phrase():
        """Abort current phrase"""
        global ts_threshold
        ts_threshold = time.perf_counter()


def on_phrase(phrase):
    global ts_threshold
    if not actions.speech.enabled():
        return

    words = phrase.get("text")
    if not words:
        return

    if ts_threshold is not None and phrase.get("_ts") < ts_threshold:
        ts_threshold = None
        phrase["parsed"]._sequence = []
        return

    is_aborted, text = actions.user.abort_phrase(phrase, words)
    if not is_aborted:
        is_sleep, text = actions.user.talon_sleep_update_phrase(words)
        if not is_sleep:
            text = " ".join(words)

    actions.user.print_phrase_timings(phrase, text)
    actions.user.subtitle(text)
    actions.user.command_history_append(text)


speech_system.register("phrase", on_phrase)
