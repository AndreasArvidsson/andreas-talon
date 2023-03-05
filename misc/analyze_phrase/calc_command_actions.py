from talon import Module, Context, actions, registry, app
from talon.grammar import Phrase
from talon_init import TALON_HOME
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
PARAM_RE = re.compile(r"\{(.*?)\}")
OR_RE = re.compile(r"(.+) or (.+)")

ignore_actions = {
    "sleep",
}

default_descs = {
    "insert": "Insert text <text>",
    "auto_insert": "Insert text <text>",
    "print": "Log text <obj>",
    "user.vscode": "Execute vscode command <command_id>",
    "user.vscode_get": "Execute vscode command <command_id> with return value",
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
            [
                AnalyzedCommandWithActions(
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
        parameters_map = get_parameters(command)
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
            action_args = inspect.getfullargspec(action.func).args
            path = get_path(inspect.getsourcefile(action.func))

            try:
                line_number = inspect.getsourcelines(action.func)[1]
            except:
                line_number = None

            mod_desc = action.type_decl.desc
            ctx_desc = (
                inspect.getdoc(action.func) if isinstance(action.ctx, Context) else None
            )

            if action_params:
                explanation = get_action_explanation(
                    action_name,
                    action_params,
                    action_args,
                    mod_desc,
                    ctx_desc,
                    parameters_map,
                )
            else:
                explanation = None

            actions.append(
                AnalyzedAction(
                    line,
                    action_name,
                    action_params,
                    path,
                    line_number,
                    mod_desc,
                    ctx_desc,
                    explanation,
                )
            )

        return actions


def get_parameters(command: AnalyzedCommand):
    parameters = {}

    for capture, values in command.captureMapping.items():
        parameters[f"{capture}_list"] = values
        parameters[capture] = values[0]
        for i, value in enumerate(values):
            parameters[f"{capture}_{i+1}"] = value

    return parameters


def get_action_explanation(
    action_name: str,
    action_params: str,
    action_args: list[str],
    mod_desc: str,
    ctx_desc: str,
    parameters_map: dict,
) -> Union[str, None]:
    if action_name == "key":
        keys = update_parameter(action_params, parameters_map)
        is_plural = len(keys) > 1 and " " in keys or "-" in keys
        label = "keys" if is_plural else "key"
        return f"Press {label} '{keys}'"

    action_params = [x.strip() for x in action_params.split(",")]
    action_desc = ctx_desc or default_descs.get(action_name) or mod_desc

    result = action_desc
    length = min(len(action_params), len(action_args))

    for param, arg in zip(action_params[:length], action_args[:length]):
        value = update_parameter(param, parameters_map)
        result = result.replace(f"<{arg}>", f"'{value}'")

    result = result.replace("\n", "\\n")

    if result != action_desc:
        return result

    return None


def update_parameter(param: str, map: dict) -> str:
    if is_string(param):
        for p in set(PARAM_RE.findall(param)):
            param = param.replace(f"{{{p}}}", update_parameter(p, map))
        return destring(param)

    if param in map:
        return str(map[param])

    or_match = OR_RE.match(param)
    if or_match:
        param = or_match.group(1)
        default_value = or_match.group(2)
        if param in map:
            return str(map[param])
        return update_parameter(default_value, map)

    return param


def is_string(text: str) -> bool:
    return STRING_RE.match(text) is not None


def destring(text: str) -> str:
    return text[1:-1]


def get_path(filename: str) -> str:
    return os.path.relpath(filename, TALON_HOME)


def test_get_action_explanation():
    def get_print(name: str, params: str, expected: str = None):
        return [
            name,
            "print",
            params,
            ["obj"],
            "Module description",
            None,
            {"prose": "hello world"},
            f"Log text '{expected or 'hello world'}'",
        ]

    def get_key(name: str, params: str, expected: str):
        return [
            name,
            "key",
            params,
            ["key"],
            "Module description",
            None,
            {"letter": "a b"},
            expected,
        ]

    def get_vscode(name: str, expected: str = ""):
        return [
            name,
            f"user.{name}",
            "edit.command",
            ["command_id"],
            "Module description",
            None,
            {},
            f"Execute vscode command 'edit.command'" + expected,
        ]

    def get_desc(name: str, mod: str, ctx: str, expected: str):
        return [name, "my_action", "hello world", ["text"], mod, ctx, {}, expected]

    fixtures = [
        get_print("print1", "hello world"),
        get_print("print2", "prose"),
        get_print("print3", "'{prose}'"),
        get_print("print4", '"{prose}"'),
        get_print("print5", '"say {prose}!"', "say hello world!"),
        [
            "print6",
            "print",
            "\"a {number_small} b {number_small_2 or 'X'} c {number_small}\"",
            ["obj"],
            "Module description",
            None,
            {"number_small": 1},
            "Log text 'a 1 b X c 1'",
        ],
        [
            "print7",
            "print",
            "\"a {number_small} b {number_small_2 or 'X'} c {number_small}\"",
            ["obj"],
            "Module description",
            None,
            {"number_small": 1, "number_small_2": 2},
            "Log text 'a 1 b 2 c 1'",
        ],
        get_key("key1", "a", "Press key 'a'"),
        get_key("key2", "a b", "Press keys 'a b'"),
        get_key("key3", "ctrl-a", "Press keys 'ctrl-a'"),
        get_key("key4", "letter", "Press keys 'a b'"),
        get_key("key5", "'{letter}'", "Press keys 'a b'"),
        get_key("key6", '"{letter}"', "Press keys 'a b'"),
        get_key("key7", '"{letter} c"', "Press keys 'a b c'"),
        get_vscode("vscode"),
        get_vscode("vscode_get", " with return value"),
        get_desc(
            "mod desc",
            "Module description <text>",
            None,
            "Module description 'hello world'",
        ),
        get_desc(
            "ctx desc",
            "Module description <text>",
            "Context description <text>",
            "Context description 'hello world'",
        ),
        [
            "formatter",
            "my_action",
            'prose, "ALL_CAPS"',
            ["text", "formatters"],
            "Module description",
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
