# https://github.com/pokey/wax_talon/blob/697e94add6316e6de700a3e228480a4e847baa59/parse_sim.py
import re

from talon import Module, app
from talon_init import TALON_HOME

mod = Module()


@mod.action_class
class Actions:
    def parse_sim(sim: str):
        """Attempts to parse {sim} (the output of `sim()`) into a richer object with the phrase, grammar, path,
        and possibly the matched rule(s).
        """
        results = SIM_RE.findall(sim)

        if not results:
            return None

        commands = []

        for str, num, phrase, path, rule in results:
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
