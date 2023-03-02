from talon import Module, actions, registry, app
from talon.grammar import Phrase
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
    def analyze_phrase_with_actions(phrase: Phrase) -> AnalyzedPhraseWithActions:
        """Analyze spoken phrase. Include actions"""
        analyzed_phrase: AnalyzedPhrase = actions.user.analyze_phrase(phrase)

        return AnalyzedPhraseWithActions(
            analyzed_phrase.phrase,
            analyzed_phrase.words,
            analyzed_phrase.metadata,
            analyzed_phrase.rawSim,
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
                for cmd in analyzed_phrase.commands
            ],
        )

    def calc_command_actions(command: AnalyzedCommand) -> list[AnalyzedAction]:
        """Calculate command actions from a analyzed phrase"""
        lines = [l for l in command.code.splitlines() if l and not l.startswith("#")]
        parametersMap = get_parameters(command)
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

            modDesc = action.type_decl.desc
            ctxDesc = inspect.getdoc(action.func)

            if action_params:
                explanation = get_action_explanation(
                    action_name,
                    action_params,
                    inspect.getfullargspec(action.func).args,
                    ctxDesc or modDesc,
                    parametersMap,
                )
            else:
                explanation = None

            actions.append(
                AnalyzedAction(
                    line,
                    action_name,
                    action_params,
                    action.ctx.path.replace(".", os.path.sep),
                    lineNumber,
                    modDesc,
                    ctxDesc,
                    explanation,
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
    action_name: str,
    action_params: str,
    action_args: list[str],
    action_desc: str,
    parametersMap: dict,
) -> Union[str, None]:
    if action_name == "key":
        keys = apply_parameters(action_params, parametersMap, key_replacements)
        is_plural = " " in keys or "-" in keys
        label = "keys" if is_plural else "key"
        return f"Press {label} '{keys}'"

    if action_name == "insert" or action_name == "auto_insert":
        text = apply_parameters(action_params, parametersMap)
        return f"Insert text '{text}'"

    if action_name == "print":
        text = apply_parameters(action_params, parametersMap)
        return f"Log text '{text}'"

    if action_name == "user.vscode_get":
        return f"Execute vscode command '{destring(action_params)}' with return value"

    if action_name == "user.vscode":
        return f"Execute vscode command '{destring(action_params)}'"

    if len(action_args):
        action_params = [x.strip() for x in action_params.split(",")]

        if len(action_args) == len(action_params):
            result = action_desc

            for param, arg in zip(action_params, action_args):
                if is_string(param):
                    value = apply_parameters(param, parametersMap)
                elif param in parametersMap:
                    value = parametersMap[param]
                else:
                    value = destring(param)
                result = result.replace(f"<{arg}>", f"'{value}'")

            if result != action_desc:
                return result
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


def test_get_action_explanation():
    def get_print(name: str, params: str, expected: str = None):
        return [
            name,
            "print",
            params,
            None,
            None,
            {"prose": "hello world"},
            f"Log text '{expected or 'hello world'}'",
        ]

    def get_key(name: str, params: str, expected: str):
        return [name, "key", params, None, None, {"letter": "a b"}, expected]

    def get_vscode(name: str, expected: str = ""):
        return [
            name,
            f"user.{name}",
            "edit.command",
            None,
            None,
            None,
            f"Execute vscode command 'edit.command'" + expected,
        ]

    fixtures = [
        get_print("print1", "hello world"),
        get_print("print2", "prose"),
        get_print("print3", "'{prose}'"),
        get_print("print4", '"{prose}"'),
        get_print("print5", '"say {prose}!"', "say hello world!"),
        get_key("key1", "a", "Press key 'a'"),
        get_key("key2", "a b", "Press keys 'a b'"),
        get_key("key3", "ctrl-a", "Press keys 'ctrl-a'"),
        get_key("key4", "letter", "Press keys 'a b'"),
        get_key("key5", "'{letter}'", "Press keys 'a b'"),
        get_key("key6", '"{letter}"', "Press keys 'a b'"),
        get_key("key7", '"{letter} c"', "Press keys 'a b c'"),
        get_vscode("vscode"),
        get_vscode("vscode_get", " with return value"),
        [
            "doc string1",
            "my_action",
            'prose, "ALL_CAPS"',
            ["text", "formatters"],
            "Insert text <text> formatted as <formatters>",
            {"prose": "hello world"},
            "Insert text 'hello world' formatted as 'ALL_CAPS'",
        ],
    ]

    def test(fixture):
        params = fixture[1:-1]
        expected = fixture[-1]
        found = get_action_explanation(*params)
        actions.user.assert_equals(expected, found)

    actions.user.test_run_suite("get_action_explanation", fixtures, test)


# app.register("ready", test_get_action_explanation)
