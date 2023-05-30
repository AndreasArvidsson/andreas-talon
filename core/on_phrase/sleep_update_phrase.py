from talon.grammar import Phrase
from ..modes.modes import sleep_phrases


def sleep_update_phrase(phrase: Phrase) -> tuple[bool, str]:
    """Update spoken phrase in case of sleep command"""
    words = phrase["phrase"]

    for sleep_phrase in sleep_phrases:
        if sleep_phrase in words:
            index = words.index(sleep_phrase)
            text = " ".join(words[: index + 1])
            phrase["phrase"] = words[: index + 1]
            if index < len(words) - 1:
                text += " ..."
            return True, text

    return False, " ".join(words)
