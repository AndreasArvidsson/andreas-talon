from talon import Module, speech_system, registry
from talon.grammar import Capture
from typing import Union
import re
from dataclasses import dataclass
import os

mod = Module()

SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")
ACTION_RE = re.compile(r"(?:.*\s)?([\w.]+)\((.*?)\)")
PARAM_RE = re.compile(r"[{<](.+)[}>]")
STRING_RE = re.compile(r"""^".*"$|^'.*'$""")

replace_values = {
    " ": "space",
}

ignore_actions = {
    "sleep",
}


def apply_parameters(action_params: str, parameters: dict) -> str:
    if is_string(action_params):
        action_params = destring(action_params)
        for k, v in parameters.items():
            action_params = action_params.replace(f"{{{k}}}", str(v))
    else:
        for k, v in parameters.items():
            action_params = action_params.replace(k, str(v))
    return action_params


def get_explanation(
    action_name: str, action_params: str, parameters: dict
) -> Union[str, None]:
    if action_name == "key":
        keys = apply_parameters(action_params, parameters)
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
        return (
            f"Execute command '{destring(action_params)}' in vscode and return results"
        )

    if action_name == "user.vscode":
        return f"Execute command '{destring(action_params)}' in vscode"

    return None


@dataclass
class SimAction:
    name: str
    desc: str


class SimCommand:
    def __init__(
        self,
        num: int,
        phrase: str,
        path: str,
        rule: str,
        parameters: dict,
        actions: list[SimAction],
    ):
        self.num = num
        self.phrase = phrase
        self.path = path
        self.rule = rule
        self.parameters = parameters
        self.actions = actions
        self.name = path[path.rindex(os.path.sep) + 1 : -6]


@mod.action_class
class Actions:
    def simulate_phrase(phrase: dict, text: str, is_aborted: bool) -> list:
        """Simulate spoke phrase and return list of commands"""
        try:
            if is_aborted:
                return [aborted_command(text)]

            return parse_sim(phrase)
        except Exception as e:
            print("Failed to simulate phrase")
            print(e)
            return []


def aborted_command(phrase: str) -> SimCommand:
    name = "abort.talon"
    action_name = "user.abort_phrase"

    context_name = next(x for x in registry.contexts.keys() if x.endswith(name))
    path_prefix = os.path.sep.join(context_name.split(".")[:-2])
    path = f"{path_prefix}{os.path.sep}{name}"

    context = registry.contexts[context_name]
    command_key = next(iter(context.commands))
    command = context.commands[command_key]

    action = SimAction(
        action_name,
        get_action_description(action_name),
    )

    return SimCommand(
        1,
        phrase,
        path,
        command.rule.rule,
        [action],
    )


def parse_sim(phrase: dict) -> list[SimCommand]:
    """Attempts to parse {sim} (the output of `sim()`) into a richer object with the phrase, grammar, path,
    and possibly the matched rule(s).
    """
    text = " ".join(phrase["text"])
    parsed = phrase["parsed"]
    sim = speech_system._sim(text)
    matches = SIM_RE.findall(sim)

    if not matches:
        return None

    commands = []
    i = 0

    for _, num, phrase, path, rule in matches:
        parameters = parse_capture(rule, parsed[i])
        commands.append(
            SimCommand(
                int(num),
                phrase,
                path,
                rule,
                parameters,
                get_actions(phrase, path, rule, parameters),
            )
        )
        i += 1

    return commands


def get_actions(phrase: str, path: str, rule: str, parameters: dict) -> list[SimAction]:
    context_name = path_to_context_name(path)
    context = registry.contexts[context_name]
    commands = context.commands.values()
    command = next(x for x in commands if x.rule.rule == rule)
    lines = command.target.code.splitlines()
    actions = []

    for line in lines:
        match = ACTION_RE.match(line)

        if match:
            action_name = match.group(1)
            action_params = match.group(2)
        elif is_string(line):
            action_name = "auto_insert"
            action_params = line
        else:
            continue

        if action_name in ignore_actions:
            continue

        explanation = get_explanation(action_name, action_params, parameters)
        actions.append(
            SimAction(
                action_name,
                explanation or get_action_description(action_name),
            )
        )

    return actions


def parse_capture(rule: str, parsed: Capture) -> dict:
    result = {}
    rule_parts = rule.split()
    for i, value in enumerate(parsed):
        param = rule_parts[i]
        if value != param:
            name = PARAM_RE.match(param).group(1)
            name_short = name.split(".")[-1]
            if value in replace_values:
                value = replace_values[value]
            result[name_short] = value
    return result


def get_action_description(name: str) -> str:
    if name in registry.actions:
        action = registry.actions[name][0]
        return action.type_decl.desc
    raise Exception(f"Can't find action {name}")


def path_to_context_name(path: str) -> str:
    return path.replace("/", ".").replace("\\", ".")


def is_string(text: str) -> bool:
    return STRING_RE.match(text) is not None


def destring(text: str) -> str:
    if is_string(text):
        return text[1:-1]
    return text
