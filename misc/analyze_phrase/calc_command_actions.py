from talon import Module, actions, registry
from typing import Union, Optional
import re
import os
import inspect
from .types import (
    AnalyzedPhrase,
    AnalyzedCommand,
    AnalyzedPhraseWithActions,
    AnalyzedCommandWithActions,
    AnalyzedAction,
)

mod = Module()

ACTION_RE = re.compile(r"(?:.*\s)?([\w.]+)\((.*?)\)")
STRING_RE = re.compile(r"""^".*"$|^'.*'$""")

ignore_actions = {
    "sleep",
}

key_replacements = {
    " ": "space",
}


@mod.action_class
class Actions:
    def calc_analyzed_phrase_with_actions(
        phrase: AnalyzedPhrase,
    ) -> AnalyzedPhraseWithActions:
        """Turn an analyzed phrase into an analyzed phrase with actions"""

        return AnalyzedPhraseWithActions(
            phrase.phrase,
            phrase.words,
            phrase.rawSim,
            [
                AnalyzedCommandWithActions(
                    cmd.num,
                    cmd.phrase,
                    cmd.rule,
                    cmd.code,
                    cmd.path,
                    cmd.line,
                    cmd.captures,
                    cmd.captureMapping,
                    actions.user.calc_command_actions(cmd),
                )
                for cmd in phrase.commands
            ],
        )

    def calc_command_actions(command: AnalyzedCommand) -> list[AnalyzedAction]:
        """Calculate command actions from a analyzed phrase"""
        lines = [l for l in command.code.splitlines() if l and not l.startswith("#")]
        parameters = get_parameters(command)
        actions = []

        for line in lines:
            match = ACTION_RE.match(line)

            if match:
                action_name = match.group(1)
                action_params = match.group(2) or None
            elif is_string(line):
                action_name = "auto_insert"
                action_params = line
            else:
                continue

            if action_name in ignore_actions:
                continue

            if action_name not in registry.actions:
                raise Exception(f"Can't find action {action_name}")

            action = registry.actions[action_name][-1]

            try:
                lineNumber = inspect.getsourcelines(action.func)[1]
            except:
                lineNumber = None

            actions.append(
                AnalyzedAction(
                    line,
                    action_name,
                    action_params,
                    action.ctx.path.replace(".", os.path.sep),
                    lineNumber,
                    action.type_decl.desc,
                    action.func.__doc__,
                    get_action_explanation(action_name, action_params, parameters),
                )
            )

        return actions


def get_parameters(command: AnalyzedCommand):
    parameters = {}

    for capture, values in command.captureMapping.items():
        parameters[f"{capture}_list"] = values
        if len(values) == 1:
            parameters[capture] = values[0]
        else:
            for i, value in enumerate(values):
                parameters[f"{capture}_{i+1}"] = value

    return parameters


def get_action_explanation(
    action_name: str, action_params: str, parameters: dict
) -> Union[str, None]:
    if action_name == "key":
        keys = apply_parameters(action_params, parameters, key_replacements)
        is_plural = " " in keys or "-" in keys
        label = "keys" if is_plural else "key"
        return f"Press {label} '{keys}'"

    if action_name == "insert" or action_name == "auto_insert":
        text = apply_parameters(action_params, parameters)
        return f"Insert text '{text}'"

    if action_name == "print":
        text = apply_parameters(action_params, parameters)
        return f"Log text '{text}'"

    if action_name == "user.vscode_get":
        return f"Execute vscode command '{destring(action_params)}' with return value"

    if action_name == "user.vscode":
        return f"Execute vscode command '{destring(action_params)}'"

    return None


def apply_parameters(
    text: str, parameters: dict, replacements: Optional[dict] = {}
) -> str:
    was_string = is_string(text)

    if was_string:
        text = destring(text)

    for k, v in parameters.items():
        v = str(v)
        if v in replacements:
            v = replacements[v]
        if was_string:
            text = text.replace(f"{{{k}}}", v)
        else:
            text = text.replace(k, v)

    return text


def is_string(text: str) -> bool:
    return STRING_RE.match(text) is not None


def destring(text: str) -> str:
    if is_string(text):
        return text[1:-1]
    return text
