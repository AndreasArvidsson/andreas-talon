from talon import Module, speech_system, actions
from talon.grammar import Phrase

mod = Module()


def on_pre_phrase(phrase: Phrase):
    if skip_phrase(phrase):
        return

    is_aborted, text = actions.user.abort_phrase(phrase)

    if not is_aborted:
        is_sleep, text = actions.user.talon_sleep_update_phrase(phrase)

    if text:
        actions.user.subtitle(text)
        actions.user.print_phrase_timings(phrase)


def on_post_phrase(phrase: Phrase):
    if skip_phrase(phrase):
        return

    analyzed_phrase = actions.user.analyze_phrase_with_actions(phrase)
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
