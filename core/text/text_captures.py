from talon import Module, Context, actions

mod = Module()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""


@mod.capture(rule="(spell | {user.letter}) {user.letter}+")
def spell(m) -> str:
    """Spell word phoneticly"""
    return "".join(m.letter_list)


@mod.capture(rule="(<number_small> | one hundred) percent")
def percent(m) -> str:
    """Percent number"""
    try:
        number = m.number_small
    except AttributeError:
        number = 100
    return f"{number}%"


@mod.capture(rule="clip clip")
def clipboard(m) -> str:
    """Clipboard content"""
    return actions.clip.text()


@ctx_sv.capture("user.clipboard", rule="klipp klipp | klippklipp")
def clipboard_sv(m) -> str:
    return actions.clip.text()


@mod.capture(rule="blah")
def placeholder(m) -> str:
    """Placeholder word"""
    return "PLACEHOLDER"
