from talon import Module, actions, speech_system, registry
from talon.grammar import Phrase, Capture
from talon.grammar.vm import VMListCapture, VMCapture
from talon.engines.w2l import DecodeWord, WordMeta
from talon.scripting.types import CommandImpl
from talon_init import TALON_HOME
from typing import Optional
import os
import re
from .types import AnalyzedPhrase, AnalyzedCommand, AnalyzedCapture, AnalyzedWord

SIM_RE = re.compile(r"""(?:\[\d+] "[^"]+"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")

mod = Module()


@mod.action_class
class Actions:
    def analyze_phrase(phrase: Phrase) -> AnalyzedPhrase:
        """Analyze spoken phrase"""
        phrase_text = get_phrase(phrase)
        return AnalyzedPhrase(
            phrase_text,
            get_words(phrase),
            get_metadata(phrase),
            get_commands(phrase, phrase_text),
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


def get_commands(phrase: Phrase, phrase_text: str) -> list[AnalyzedCommand]:
    captures = phrase["parsed"]
    commands = get_commands_impl(captures, phrase_text)
    cmd = commands[0]

    return [
        AnalyzedCommand(
            " ".join(capture._unmapped),
            command.rule.rule,
            command.target.code,
            get_path(command.target.filename),
            command.target.start_line,
            get_captures(capture),
            get_capture_mapping(capture),
        )
        for command, capture in zip(commands, captures)
    ]


def get_commands_impl(captures: list[Capture], phrase_text: str) -> list[CommandImpl]:
    commands = try_get_last_commands(captures)
    if commands:
        return commands
    commands = get_commands_from_sim(phrase_text)
    if len(captures) != len(commands):
        raise Exception(
            f"Got in correct number of commands({len(commands)}) for the list of captures({len(captures)})"
        )
    return commands


def try_get_last_commands(captures: list[Capture]) -> Optional[list[CommandImpl]]:
    """
    Returns last command implementation if its captures matches the given list.
    Repeat commands are missing from this list and then we can't use the list of last commands.
    """
    recent_commands = actions.core.recent_commands()
    if not recent_commands:
        return None
    last_commands = recent_commands[-1]
    if len(captures) != len(last_commands):
        return None
    for c1, (_, c2) in zip(captures, last_commands):
        if c1 != c2:
            return None
    return [cmd for cmd, _ in last_commands]


def get_commands_from_sim(phrase_text: str) -> list[CommandImpl]:
    try:
        raw_sim = speech_system._sim(phrase_text)
    except Exception as ex:
        raise Exception(f"Failed to run sim on phrase '{phrase_text}'. Ex: {ex}")

    matches = SIM_RE.findall(raw_sim)
    if not matches:
        raise Exception(f"Can't parse sim '{raw_sim}'")

    return [get_command_from_path(path, rule) for path, rule in matches]


def get_command_from_path(path: str, rule: str) -> CommandImpl:
    context_name = path.replace(os.path.sep, ".")
    if not context_name in registry.contexts:
        raise Exception(f"Can't find context for path '{path}'")
    context = registry.contexts[context_name]
    commands = [c for c in context.commands.values() if c.rule.rule == rule]
    if len(commands) != 1:
        raise Exception(
            f"Expected 1 command. Found {len(commands)} for rule '{rule}' in path '{path}'"
        )
    return commands[0]


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
