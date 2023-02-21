from talon import Module, speech_system, registry
from talon.grammar import Phrase, Capture
import re
import os
from .types import AnalyzedPhrase, AnalyzedCommand, WordTiming

mod = Module()

SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")
PARAM_RE = re.compile(r"[{<](.+)[}>]")


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
        parameters = get_parameters_from_capture(rule, capture)
        commands.append(
            AnalyzedCommand(
                int(num),
                phrase,
                path,
                rule,
                command.target.code,
                command.target.start_line,
                list(capture),
                parameters,
            )
        )

    return commands


def get_command(path: str, rule: str):
    context_name = path.replace(os.path.sep, ".")
    context = registry.contexts[context_name]
    commands = context.commands.values()
    return next(x for x in commands if x.rule.rule == rule)


def get_parameters_from_capture(rule: str, capture: Capture) -> dict:
    result = {}
    rule_parts = rule.split()
    count = {}

    for i, value in enumerate(capture):
        param = rule_parts[i]
        if value != param:
            match = PARAM_RE.match(param)

            if not match:
                continue

            name = match.group(1)
            name_short = name.split(".")[-1]

            if param in count:
                count[param] += 1
            else:
                count[param] = 1
                result[name_short] = value
            result[f"{name_short}_{count[param]}"] = value

    return result
