from talon import Module, speech_system, registry
from talon.grammar import Phrase, Capture
import re
import os
from .types import AnalyzedPhrase, AnalyzedCommand, AnalyzedCapture, AnalyzedWord

mod = Module()

SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")


@mod.action_class
class Actions:
    def analyze_phrase(phrase: Phrase) -> AnalyzedPhrase:
        """Analyze spoken phrase"""
        words = phrase.get("phrase")
        phrase_text = " ".join(words)
        raw_sim = speech_system._sim(phrase_text)

        return AnalyzedPhrase(
            phrase_text,
            get_word_timings(words),
            raw_sim,
            get_commands(phrase, raw_sim),
        )


def get_word_timings(words: list) -> list[AnalyzedWord]:
    return [
        AnalyzedWord(str(word), word.start, word.end)
        for word in words
    ]


def get_commands(phrase: Phrase, raw_sim: str) -> list[AnalyzedCommand]:
    parsed = phrase["parsed"]
    matches = SIM_RE.findall(raw_sim)
    commands = []

    if not matches:
        raise Exception("Failed to run sim on phrase")

    for _, num, phrase, path, rule in matches:
        command = get_command(path, rule)
        capture = parsed[len(commands)]
        commands.append(
            AnalyzedCommand(
                int(num),
                phrase,
                path,
                rule,
                command.target.code,
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

    for i in range(len(capture._unmapped)):
        phrase = capture._unmapped[i]
        value = capture._sequence[i]

        c = capture._capture[i]
        try:
            name = c._name
        except AttributeError:
            name = c

        captures.append(AnalyzedCapture(phrase, name, value))

    return captures


def get_capture_mapping(capture: Capture):
    mapping = {}

    for k, v in capture._mapping.items():
        if not k.endswith("_list") and not "." in k:
            mapping[k] = v

    return mapping
