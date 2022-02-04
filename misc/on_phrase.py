from talon import speech_system, actions


def on_phrase(d):
    if not actions.speech.enabled():
        return

    words = d.get("text")
    if not words:
        return

    is_aborted, text = actions.user.abort_phrase(d, words)
    if not is_aborted:
        is_sleep, text = actions.user.talon_sleep_update_phrase(words)
        if not is_sleep:
            text = " ".join(words)

    actions.user.print_phrase_timings(d, text)
    actions.user.subtitle(text)
    actions.user.command_history_append(text)


speech_system.register("phrase", on_phrase)
