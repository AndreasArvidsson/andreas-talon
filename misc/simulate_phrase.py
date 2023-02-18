import re
from talon import Module, speech_system, registry

mod = Module()


@mod.action_class
class Actions:
    def simulate_phrase(phrase: str, is_aborted: bool) -> list:
        """Simulate spoke phrase and return list of commands"""
        try:
            if is_aborted:
                return [canceled_command(phrase)]

            sim = speech_system._sim(phrase)
            commands = parse_sim(sim)
            add_actions(commands)
            return commands
        except Exception as e:
            print(e)
            return []


def canceled_command(phrase: str):
    path = "user\\andreas-talon\\misc\\abort\\abort.talon"
    action_name = "user.abort_phrase"
    action_desc = get_action_description(action_name)

    # context_name = path_to_context_name(path)
    # context = registry.contexts[context_name]
    # commands = next(context.commands)
    # print(commands)

    return {
        "num": 1,
        "phrase": phrase,
        "path": path,
        "rule": "{user.abort_phrase}$",
        "actions": [
            {
                "name": action_name,
                "desc": action_desc,
            }
        ],
    }


def add_actions(sim_commands: list):
    """Enrich simulated commands with action"""

    for sim_cmd in sim_commands:
        context_name = path_to_context_name(sim_cmd["path"])
        rule = sim_cmd["rule"]

        context = registry.contexts[context_name]
        commands = context.commands.values()
        command = next(x for x in commands if x.rule.rule == rule)

        actions = []

        for line in command.target.lines:
            action_name = get_action_name(line)
            action_desc = get_action_description(action_name)
            actions.append(
                {
                    "name": action_name,
                    "desc": action_desc,
                }
            )

        sim_cmd["actions"] = actions


def path_to_context_name(path: str):
    return path.replace("\\", ".")


def get_action_description(name: str):
    if name in registry.actions:
        action = registry.actions[name][0]
        return action.type_decl.desc
    raise Exception(f"Can't find action {name}")


def get_action_name(command_line: dict):
    name = getattr(command_line, "name", None)
    if name:
        return name
    keys = getattr(command_line, "keys", None)
    if keys:
        return "key"
    raise Exception(f"Can't find action name: {command_line}")


def parse_sim(sim: str):
    """Attempts to parse {sim} (the output of `sim()`) into a richer object with the phrase, grammar, path,
    and possibly the matched rule(s).
    """
    matches = SIM_RE.findall(sim)

    if not matches:
        return None

    commands = []

    for _, num, phrase, path, rule in matches:
        commands.append(
            {
                "num": int(num),
                "phrase": phrase,
                "path": path,
                "rule": rule,
            }
        )

    return commands


SIM_RE = re.compile(r"""(\[(\d+)] "([^"]+)"\s+path: ([^\n]+)\s+rule: "([^"]+))+""")
