from talon import Module

mod = Module()

mod.tag("code_keywords")

mod.list("code_keyword", "Names of miscellaneous text insertions")


@mod.capture(rule="{user.code_keyword}+")
def code_keywords(m) -> str:
    """Returns multiple code inserts join together"""
    return " ".join(m.code_keyword_list).replace("  ", " ")
