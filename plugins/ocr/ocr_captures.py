from dataclasses import dataclass
from typing import Optional

from talon import Module, actions
from talon.grammar import Phrase

mod = Module()


@dataclass
class TimestampedText:
    text: str
    start: float
    end: float


@mod.capture(rule="<phrase> | {user.vocabulary}")
def timestamped_phrase_default(m) -> TimestampedText:
    """Dictated phrase appearing onscreen (default capture)."""
    item = m[0]
    if isinstance(item, Phrase):
        text = " ".join(
            actions.dictate.replace_words(actions.dictate.parse_words(item))
        )
        start = item.words[0].start
        end = item.words[-1].end
    else:
        text = str(item)
        start = item.start
        end = item.end
    return TimestampedText(text=text, start=start, end=end)
