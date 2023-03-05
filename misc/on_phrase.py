from talon import speech_system, actions
from talon.grammar import Phrase


def on_phrase(phrase: Phrase):
    if not actions.speech.enabled() or not phrase.get("phrase"):
        return

    is_aborted, text = actions.user.abort_phrase(phrase)

    if not is_aborted:
        is_sleep, text = actions.user.talon_sleep_update_phrase(phrase)

    if text:
        actions.user.subtitle(text)
        actions.user.print_phrase_timings(phrase, text)


def on_post_phrase(phrase: Phrase):
    if not actions.speech.enabled() or not phrase.get("phrase"):
        return

    analyzed_phrase = actions.user.analyze_phrase_with_actions(phrase)
    actions.user.command_history_append(analyzed_phrase)
    actions.user.pretty_print_phrase(analyzed_phrase)
    print(analyzed_phrase)


speech_system.register("phrase", on_phrase)
speech_system.register("post:phrase", on_post_phrase)
