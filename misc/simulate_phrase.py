import re
from talon import Module, speech_system

mod = Module()


@mod.action_class
class Actions:
    def simulate_phrase(phrase: str) -> list:
        """Simulate spoke phrase and return list of commands"""
        sim = speech_system._sim(phrase)
        return parse_sim(sim)


def parse_sim(sim: str):
    """Attempts to parse {sim} (the output of `sim()`) into a richer object with the phrase, grammar, path,
    and possibly the matched rule(s).
    """
    results = SIM_RE.findall(sim)

    if not results:
        return None

    commands = []

    for _, num, phrase, path, rule in results:
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
