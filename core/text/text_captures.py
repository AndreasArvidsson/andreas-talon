from talon import Module


mod = Module()


@mod.capture(rule="(spell | {user.letter}) {user.letter}+")
def spell(m) -> str:
    """Spell word phoneticly"""
    return "".join(m.letter_list)


@mod.capture(rule="time <number_small> (<number_small> | oh {user.digit} | o'clock)")
def time(m) -> str:
    """24 hour time"""
    hours = str(m.number_small)
    try:
        minutes = str(m.number_small_2)
    except AttributeError:
        try:
            minutes = str(m.digit)
        except AttributeError:
            minutes = ""
    return f"{hours.rjust(2,'0')}:{minutes.rjust(2,'0')}"


@mod.capture(rule="<number_small> percent")
def percent(m) -> str:
    """Percentages"""
    return f"{m.number_small}%"


@mod.capture(rule="blah")
def placeholder(m) -> str:
    """Placeholder word"""
    return "PLACEHOLDER"
