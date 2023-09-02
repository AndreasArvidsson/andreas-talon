from talon import Module

mod = Module()

mod.tag("code_inserts")

mod.list("code_insert", "Names of miscellaneous text insertions")


@mod.capture(rule="{user.code_insert}+")
def code_inserts(m) -> str:
    """Returns multiple code inserts join together"""
    return " ".join(m.code_insert_list).replace("  ", " ")
