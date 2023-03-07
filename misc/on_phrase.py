from talon import Module, speech_system, actions
from talon.grammar import Phrase

mod = Module()

settings_pretty = mod.setting(
    "pretty_print_phrase",
    type=bool,
    default=False,
    desc="If true phrase will be pretty printed to the log",
)


def on_phrase(phrase: Phrase):
    if not actions.speech.enabled() or not phrase.get("phrase"):
        return

    is_aborted, text = actions.user.abort_phrase(phrase)

    if not is_aborted:
        is_sleep, text = actions.user.talon_sleep_update_phrase(phrase)

    if text:
        actions.user.subtitle(text)
        actions.user.print_phrase_timings(phrase)


def on_post_phrase(phrase: Phrase):
    if not actions.speech.enabled() or not phrase.get("phrase"):
        return

    analyzed_phrase = actions.user.analyze_phrase_with_actions(phrase)
    actions.user.command_history_append(analyzed_phrase)
    if settings_pretty.get():
        actions.user.pretty_print_phrase(analyzed_phrase)


speech_system.register("pre:phrase", on_phrase)
speech_system.register("post:phrase", on_post_phrase)
