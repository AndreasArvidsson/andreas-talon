from talon import Module, actions, speech_system, registry
from talon.grammar import Phrase, Capture
from talon.grammar.vm import Phrase, Capture, VMListCapture, VMCapture
from talon.engines.w2l import DecodeWord, WordMeta
from talon_init import TALON_HOME
from typing import Optional
import os
from .types import AnalyzedPhrase, AnalyzedCommand, AnalyzedCapture, AnalyzedWord

mod = Module()


@mod.action_class
class Actions:
    def analyze_phrase(phrase: Phrase) -> AnalyzedPhrase:
        """Analyze spoken phrase"""
        return AnalyzedPhrase(
            get_phrase(phrase),
            get_words(phrase),
            get_metadata(phrase),
            get_commands(phrase),
        )


def get_phrase(phrase: Phrase) -> str:
    return " ".join(phrase["phrase"])


def get_words(phrase: Phrase) -> list[AnalyzedWord]:
    words = phrase["phrase"]
    return [
        AnalyzedWord(
            str(word),
            getattr(word, "start", None),
            getattr(word, "end", None),
        )
        for word in words
    ]


def get_metadata(phrase: Phrase) -> Optional[dict]:
    meta = phrase.get("_metadata")
    if meta:
        # We have already captured the phrase and don't need a duplication.
        return {k: v for k, v in meta.items() if k not in {"emit", "decode"}}
    return None


def get_commands(phrase: Phrase) -> list[AnalyzedCommand]:
    commands = actions.core.recent_commands()[-1]
    captures = phrase["parsed"]

    result = []

    for i, (command, capture) in enumerate(commands):
        if capture != captures[i]:
            raise Exception(
                "Expected different capture. Make sure to use phrase from 'post:phrase' event"
            )

        result.append(
            AnalyzedCommand(
                " ".join(capture._unmapped),
                command.rule.rule,
                command.target.code,
                get_path(command.target.filename),
                command.target.start_line,
                get_captures(capture),
                get_capture_mapping(capture),
            )
        )

    return result


def get_path(filename: str) -> str:
    return os.path.relpath(filename, TALON_HOME)


def get_captures(capture: Capture) -> AnalyzedCapture:
    captures = []

    for i, value in enumerate(capture):
        c = capture._capture[i]

        if isinstance(c, DecodeWord) or isinstance(c, WordMeta):
            phrase = c.word
            name = None
        elif isinstance(c, VMCapture):
            phrase = " ".join(c.unmapped())
            name = c._name
        elif isinstance(c, VMListCapture):
            phrase = c._value
            name = c._name
        else:
            raise Exception(f"Unknown capture type '{type(c)}'")

        captures.append(AnalyzedCapture(phrase, value, name))

    return captures


def get_capture_mapping(capture: Capture):
    mapping = {}

    for k, v in capture._mapping.items():
        if not k.endswith("_list") and not "." in k:
            mapping[k] = v

    return mapping
