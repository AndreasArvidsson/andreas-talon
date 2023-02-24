from talon import Module, speech_system, registry
from talon.grammar import Phrase, Capture
from talon.grammar.vm import Phrase, Capture, VMListCapture, VMCapture
from talon.engines.w2l import DecodeWord, WordMeta
from typing import Optional
import re
import os
from .types import AnalyzedPhrase, AnalyzedCommand, AnalyzedCapture, AnalyzedWord

mod = Module()

SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")


@mod.action_class
class Actions:
    def analyze_phrase(phrase: Phrase) -> AnalyzedPhrase:
        """Analyze spoken phrase"""
        words = phrase["phrase"]
        phrase_text = " ".join(words)

        try:
            raw_sim = speech_system._sim(phrase_text)
        except Exception as ex:
            raise Exception(f"Failed to run sim on phrase '{phrase_text}'. Ex: {ex}")

        return AnalyzedPhrase(
            phrase_text,
            get_word_timings(words),
            get_metadata(phrase),
            raw_sim,
            get_commands(phrase, raw_sim),
        )


def get_metadata(phrase: Phrase) -> Optional[dict]:
    meta = phrase.get("_metadata")
    if meta:
        # We have already captured the phrase and don't need a duplication.
        return {k: v for k, v in meta.items() if k not in {"emit", "decode"}}
    return None


def get_word_timings(words: list) -> list[AnalyzedWord]:
    return [
        AnalyzedWord(
            str(word),
            getattr(word, "start", None),
            getattr(word, "end", None),
        )
        for word in words
    ]


def get_commands(phrase: Phrase, raw_sim: str) -> list[AnalyzedCommand]:
    parsed = phrase["parsed"]
    matches = SIM_RE.findall(raw_sim)
    commands = []

    if not matches:
        raise Exception(f"Can't parse sim '{raw_sim}'")

    for _, num, phrase, path, rule in matches:
        command = get_command(path, rule)
        capture = parsed[len(commands)]
        commands.append(
            AnalyzedCommand(
                int(num),
                phrase,
                rule,
                command.target.code,
                path,
                command.target.start_line,
                get_captures(capture),
                get_capture_mapping(capture),
            )
        )

    return commands


def get_command(path: str, rule: str):
    context_name = path.replace(os.path.sep, ".")
    context = registry.contexts[context_name]
    commands = context.commands.values()
    return next(x for x in commands if x.rule.rule == rule)


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
