from talon import speech_system, actions


def on_phrase(phrase):
    if not actions.speech.enabled():
        return

    words = phrase.get("text")
    if not words:
        return

    is_aborted, text = actions.user.abort_phrase(phrase, words)

    if not is_aborted:
        is_sleep, text = actions.user.talon_sleep_update_phrase(words)
        if not is_sleep:
            text = " ".join(words)

    if text:
        actions.user.print_phrase_timings(phrase, text)
        actions.user.subtitle(text)
        actions.user.command_history_append(text)


speech_system.register("phrase", on_phrase)
