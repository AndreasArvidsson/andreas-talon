from talon import Module, speech_system, registry
from typing import Union
import re
from dataclasses import dataclass
import os

mod = Module()

SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")
ACTION_RE = re.compile(r"([\w.]+)\((.*)\)")
LIST_RE = re.compile(r"\{([\w.]+)\}")

replace_map = {
    " ": "space",
}


def get_list_parameters(phrase: str, rule: str) -> dict:
    result = {}
    phrase_words = phrase.split()
    rule_words = rule.split()
    i = 0

    for rule_word in rule_words:
        match = LIST_RE.match(rule_word)

        # Match list
        if match:
            list_name = match.group(1)
            list_name_short = list_name.split(".")[-1]
            registry_list = next(iter(registry.lists[list_name]))
            i2 = i + 1
            word = phrase_words[i]

            # Greedily expand matched words. eg match "question mark" over just "question"
            while i2 < len(phrase_words):
                new_word = " ".join(phrase_words[i : i2 + 1])
                if new_word in registry_list:
                    word = new_word
                    i2 += 1
                else:
                    break

            value = registry_list[word]
            if value in replace_map:
                value = replace_map[value]

            result[list_name_short] = value
            i = i2

        # Literal or capture. For now captures will us be skipped. Hopefully they are of length one
        else:
            i += 1

    return result


def get_explanation(
    phrase: str, rule: str, action_name: str, action_params: str
) -> Union[str, None]:
    if action_name == "key":
        parameters = get_list_parameters(phrase, rule)
        keys = action_params

        for k, v in parameters.items():
            keys = keys.replace(k, v)

        multiple_keys = " " in keys or "-" in keys
        label = "keys" if multiple_keys else "key"

        return f"Press {label} '{keys}'"

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
        actions: list[SimAction],
    ):
        self.num = num
        self.phrase = phrase
        self.path = path
        self.rule = rule
        self.actions = actions
        self.name = path[path.rindex(os.path.sep) + 1 : -6]


@mod.action_class
class Actions:
    def simulate_phrase(phrase: str, is_aborted: bool) -> list:
        """Simulate spoke phrase and return list of commands"""
        try:
            if is_aborted:
                return [canceled_command(phrase)]

            sim = speech_system._sim(phrase)
            return parse_sim(sim)
        except Exception as e:
            print("Failed to simulate phrase")
            print(e)
            return []


def canceled_command(phrase: str) -> SimCommand:
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


def parse_sim(sim: str) -> list[SimCommand]:
    """Attempts to parse {sim} (the output of `sim()`) into a richer object with the phrase, grammar, path,
    and possibly the matched rule(s).
    """
    matches = SIM_RE.findall(sim)

    if not matches:
        return None

    commands = []

    for _, num, phrase, path, rule in matches:
        commands.append(
            SimCommand(
                int(num),
                phrase,
                path,
                rule,
                get_actions(phrase, path, rule),
            )
        )

    return commands


def get_actions(phrase: str, path: str, rule: str) -> list[SimAction]:
    context_name = path_to_context_name(path)

    context = registry.contexts[context_name]
    commands = context.commands.values()
    command = next(x for x in commands if x.rule.rule == rule)
    lines = command.target.code.splitlines()

    actions = []

    for line in lines:
        match = ACTION_RE.match(line)

        if not match:
            continue

        action_name = match.group(1)
        action_params = match.group(2)
        explanation = get_explanation(phrase, rule, action_name, action_params)
        actions.append(
            SimAction(
                action_name,
                explanation or get_action_description(action_name),
            )
        )

    return actions


def path_to_context_name(path: str) -> str:
    return path.replace("/", ".").replace("\\", ".")


def get_action_description(name: str) -> str:
    if name in registry.actions:
        action = registry.actions[name][0]
        return action.type_decl.desc
    raise Exception(f"Can't find action {name}")
