from talon import speech_system, actions
from talon.grammar import Phrase
from .abort.abort import abort_update_phrase
from .sleep_update_phrase import sleep_update_phrase
from .print_phrase_timings import print_phrase_timings


def on_pre_phrase(phrase: Phrase):
    if skip_phrase(phrase):
        return

    is_aborted, text = abort_update_phrase(phrase)

    if not is_aborted:
        is_sleep, text = sleep_update_phrase(phrase)

    if text:
        actions.user.subtitle(text)
        print_phrase_timings(phrase)


def on_post_phrase(phrase: Phrase):
    if skip_phrase(phrase):
        return

    analyzed_phrase = actions.user.analyze_phrase(phrase)
    actions.user.command_history_append(analyzed_phrase)
    actions.user.pretty_print_phrase(analyzed_phrase)


def skip_phrase(phrase: Phrase) -> bool:
    return not phrase.get("phrase") or skip_phrase_in_sleep(phrase)


def skip_phrase_in_sleep(phrase: Phrase) -> bool:
    """Returns true if the rule is <phrase> in sleep mode"""
    return (
        not actions.speech.enabled()
        and len(phrase["parsed"]) == 1
        and "phrase" in phrase["parsed"][0]._mapping
    )


speech_system.register("pre:phrase", on_pre_phrase)
speech_system.register("post:phrase", on_post_phrase)
