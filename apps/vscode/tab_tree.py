from talon import Module

mod = Module()

@mod.capture(rule="{self.letter} [{self.letter}]")
def tab_tree_hint(m) -> str:
    "Tab tree hint"
    return "".join(m)