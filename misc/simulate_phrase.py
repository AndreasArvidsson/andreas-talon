from talon import Module, speech_system, registry
import re
from dataclasses import dataclass
import os

mod = Module()


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
                get_actions(path, rule),
            )
        )

    return commands


def get_actions(path: str, rule: str) -> list[SimAction]:
    context_name = path_to_context_name(path)

    context = registry.contexts[context_name]
    commands = context.commands.values()
    command = next(x for x in commands if x.rule.rule == rule)

    actions = []

    for line in command.target.lines:
        action_name = get_action_name(line)
        actions.append(
            SimAction(
                action_name,
                get_action_description(action_name),
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


def get_action_name(command_line: dict) -> str:
    name = getattr(command_line, "name", None)
    if name:
        return name
    keys = getattr(command_line, "keys", None)
    if keys:
        return "key"
    raise Exception(f"Can't find action name: {command_line}")


SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")
