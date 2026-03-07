import inspect
import os
import re
from typing import Any

from talon import Context, Module, registry
from talon_init import TALON_HOME

from .types import AnalyzedAction

mod = Module()

ACTION_RE = re.compile(r"(?:.*\s)?([\w.]+)\((.*)\)\s*$")
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
    "user.cursorless_action_or_ide_command": "Execute single-target cursorless command",
}


def calc_command_actions(
    code: str, capture_mapping: dict[str, Any]
) -> list[AnalyzedAction]:
    """Calculate command actions from a analyzed phrase"""
    lines = [ln for ln in code.splitlines() if ln and not ln.startswith("#")]
    parameters_map = get_parameters(capture_mapping)
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
            raise ValueError(f"Can't find action {action_name}")

        action = registry.actions[action_name][-1]
        action_args = inspect.getfullargspec(action.func).args
        source_file_path = inspect.getsourcefile(action.func)

        if not source_file_path:
            raise ValueError(f"Can't find source file for action {action_name}")

        path = get_path(source_file_path)

        try:
            line_number = inspect.getsourcelines(action.func)[1]
        except Exception:
            line_number = None

        if action.type_decl is None:
            raise ValueError(f"Action {action_name} is missing type declaration")

        mod_desc = action.type_decl.desc

        ctx_desc = (
            inspect.getdoc(action.func) if isinstance(action.ctx, Context) else None
        )

        explanation = get_action_explanation(
            action_name,
            action_params or "",
            action_args,
            mod_desc,
            ctx_desc,
            parameters_map,
        )

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


def get_parameters(capture_mapping: dict[str, Any]):
    parameters = {}

    for capture, values in capture_mapping.items():
        parameters[f"{capture}_list"] = values
        parameters[capture] = values[0]
        for i, value in enumerate(values):
            parameters[f"{capture}_{i + 1}"] = value

    return parameters


def get_action_explanation(
    action_name: str,
    action_params_str: str,
    action_args: list[str],
    mod_desc: str,
    ctx_desc: str | None,
    parameters_map: dict,
) -> str:
    if action_name == "key":
        keys = update_parameter(action_params_str, parameters_map) or action_params_str
        is_plural = len(keys) > 1 and " " in keys or "-" in keys
        label = "keys" if is_plural else "key"
        return f"Press {label} '{keys}'"

    action_params = split_action_params(action_params_str)
    action_desc = ctx_desc or default_descs.get(action_name) or mod_desc
    length = min(len(action_params), len(action_args))

    for param, arg in zip(action_params[:length], action_args[:length]):
        value = update_parameter(param, parameters_map) or param
        action_desc = action_desc.replace(f"<{arg}>", f"'{value}'")

    return action_desc.replace("\n", "\\n")


def update_parameter(param: str, map: dict) -> str | None:
    if is_string(param):
        for p in set(PARAM_RE.findall(param)):
            value = update_parameter(p, map)
            if value is not None:
                param = param.replace(f"{{{p}}}", value)
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

    return None


def split_action_params(action_params: str) -> list[str]:
    if not action_params:
        return []

    parts: list[str] = []
    current: list[str] = []
    quote_char: str | None = None

    for char in action_params:
        if quote_char is not None:
            current.append(char)
            if char == quote_char:
                quote_char = None
            continue

        if char in {'"', "'"}:
            quote_char = char
            current.append(char)
            continue

        if char == ",":
            parts.append("".join(current).strip())
            current = []
            continue

        current.append(char)

    parts.append("".join(current).strip())
    return parts


def is_string(text: str) -> bool:
    return STRING_RE.match(text) is not None


def destring(text: str) -> str:
    return text[1:-1]


def get_path(filename: str) -> str:
    return os.path.relpath(filename, TALON_HOME)
