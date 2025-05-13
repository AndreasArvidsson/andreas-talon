from talon.grammar import Phrase
from talon import Module, Context

mod = Module()
ctx = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""

mod.list("sleep_phrase", "Phrase used to sleep Talon")

sleep_phrases = ["drowse", "sömnig"]

ctx.lists["user.sleep_phrase"] = sleep_phrases[:-1]
ctx_sv.lists["user.sleep_phrase"] = sleep_phrases


def sleep_update_phrase(phrase: Phrase) -> str:
    """Update spoken phrase in case of sleep command"""
    words = phrase["phrase"]

    for sleep_phrase in sleep_phrases:
        if sleep_phrase in words:
            index = words.index(sleep_phrase)
            phrase["phrase"] = words[: index + 1]
            text = " ".join(phrase["phrase"])
            if index < len(words) - 1:
                text += " ..."
            return text

    return " ".join(words)
