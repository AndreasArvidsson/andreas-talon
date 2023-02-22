from talon import Module, speech_system, registry
from talon.grammar import Phrase, Capture
import re
import os
from .types import AnalyzedPhrase, AnalyzedCommand, AnalyzedCapture, WordTiming

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


def get_word_timings(words: list) -> list[WordTiming]:
    return [
        WordTiming(
            str(words[i]),
            words[i].start if words[i].start is not None else None,
            words[i].end if words[i].end is not None else None,
        )
        for i in range(len(words))
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
                get_capture(capture, rule),
            )
        )

    return commands


def get_command(path: str, rule: str):
    context_name = path.replace(os.path.sep, ".")
    context = registry.contexts[context_name]
    commands = context.commands.values()
    return next(x for x in commands if x.rule.rule == rule)


def get_capture(capture: Capture, rule) -> AnalyzedCapture:
    mapping = {}

    for k, v in capture._mapping.items():
        if not k.endswith("_list") and not "." in k:
            mapping[k] = v

    return AnalyzedCapture(capture._unmapped, capture._sequence, mapping)
