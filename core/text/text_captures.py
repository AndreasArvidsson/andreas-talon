from talon import Module


mod = Module()


@mod.capture(rule="(spell | {user.letter}) {user.letter}+")
def spell(m) -> str:
    """Spell word phoneticly"""
    return "".join(m.letter_list)


@mod.capture(rule="(<number_small> | one hundred) percent")
def percent(m) -> str:
    """Percentages"""
    try:
        number = m.number_small
    except AttributeError:
        number = 100
    return f"{number}%"


@mod.capture(rule="blah")
def placeholder(m) -> str:
    """Placeholder word"""
    return "PLACEHOLDER"
