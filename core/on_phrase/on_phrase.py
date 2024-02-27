from talon import Module, speech_system, actions, settings
from talon.grammar import Phrase
from .abort.abort import abort_update_phrase
from .analyze_phrase.analyze_phrase import analyze_phrase
from .command_history.command_history import command_history_append
from .subtitles_and_notifications.subtitles_and_notifications import show_subtitle
from .pretty_print_phrase import pretty_print_phrase
from .print_phrase_timings import print_phrase_timings
from .sleep_update_phrase import sleep_update_phrase

mod = Module()

mod.setting(
    "analyze_phrase",
    type=bool,
    default=True,
    desc="If true phrase will be analyzed and added to command history",
)


def on_pre_phrase(phrase: Phrase):
    if skip_phrase(phrase):
        return

    is_aborted, text = abort_update_phrase(phrase)

    if not is_aborted:
        text = sleep_update_phrase(phrase)

    if text:
        show_subtitle(text)
        print_phrase_timings(phrase)


def on_post_phrase(phrase: Phrase):
    if not settings.get("user.analyze_phrase") or skip_phrase(phrase):
        return

    try:
        analyzed_phrase = analyze_phrase(phrase)
        command_history_append(analyzed_phrase)
        pretty_print_phrase(analyzed_phrase)
    except Exception as ex:
        print(ex)


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
