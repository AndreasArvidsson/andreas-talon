from talon import Module, speech_system, registry
from talon.grammar import Capture
from typing import Union, Optional
import re
from dataclasses import dataclass
import os

mod = Module()

SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")
ACTION_RE = re.compile(r"(?:.*\s)?([\w.]+)\((.*?)\)")
PARAM_RE = re.compile(r"[{<](.+)[}>]")
STRING_RE = re.compile(r"""^".*"$|^'.*'$""")

ignore_actions = {
    "sleep",
}

key_replacements = {
    " ": "space",
}


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
        return f"Execute command '{destring(action_params)}' in vscode and get result"

    if action_name == "user.vscode":
        return f"Execute command '{destring(action_params)}' in vscode"

    return None


@dataclass
class SimAction:
    code: str
    name: str
    params: str
    desc: str
    explanation: Union[str, None]

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


class SimCommand:
    def __init__(
        self,
        num: int,
        phrase: str,
        path: str,
        rule: str,
        code: str,
        line: int,
        captures: list,
        actions: list[SimAction],
    ):
        self.num = num
        self.phrase = phrase
        self.path = path
        self.rule = rule
        self.code = code
        self.line = line
        self.captures = captures
        self.actions = actions

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"


@mod.action_class
class Actions:
    def simulate_phrase(phrase: dict) -> list:
        """Simulate spoke phrase and return list of commands"""
        try:
            return run_sim(phrase)
        except Exception as e:
            print("Failed to simulate phrase")
            print(e)
            return []


def run_sim(phrase: dict) -> list[SimCommand]:
    """Attempts to parse {sim} (the output of `sim()`) into a richer object with the phrase, grammar, path,
    and possibly the matched rule(s).
    """
    text = " ".join(phrase["phrase"])
    parsed = phrase["parsed"]
    sim = speech_system._sim(text)
    matches = SIM_RE.findall(sim)

    if not matches:
        return None

    commands = []

    for _, num, phrase, path, rule in matches:
        command = get_command(path, rule)
        capture = parsed[len(commands)]
        commands.append(
            SimCommand(
                int(num),
                phrase,
                path,
                rule,
                command.target.code,
                command.target.start_line,
                list(capture),
                get_actions(command, rule, capture),
            )
        )

    return commands


def get_actions(command: dict, rule: str, capture: Capture) -> list[SimAction]:
    lines = [l for l in command.target.code.splitlines() if l and not l.startswith("#")]
    parameters = get_parameters_from_capture(rule, capture)
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

        actions.append(
            SimAction(
                line,
                action_name,
                action_params,
                get_action_description(action_name),
                get_action_explanation(action_name, action_params, parameters),
            )
        )

    return actions


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
                result[name_short] = str(value)
            result[f"{name_short}_{count[param]}"] = str(value)

    return result


def get_command(path: str, rule: str):
    context_name = path_to_context_name(path)
    context = registry.contexts[context_name]
    commands = context.commands.values()
    return next(x for x in commands if x.rule.rule == rule)


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


def apply_parameters(
    text: str, parameters: dict, replacements: Optional[dict] = {}
) -> str:
    was_string = is_string(text)

    if was_string:
        text = destring(text)

    for k, v in parameters.items():
        if v in replacements:
            v = replacements[v]
        if was_string:
            text = text.replace(f"{{{k}}}", v)
        else:
            text = text.replace(k, v)

    return text
