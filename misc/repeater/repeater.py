from talon import Module

mod = Module()


@mod.capture(rule="twice | trice | <number_small> times")
def repeater_phrase(m) -> int:
    """Repeater string. Returns an integer for number of times to repeat"""
    if m[0] == "twice":
        return 1
    if m[0] == "trice":
        return 2
    return m.number_small - 1


@mod.capture(rule="<user.repeater_phrase> | breed")
def repeater_phrase_all(m) -> int:
    """Repeater string. Returns an integer for number of times to repeat, including all"""
    if m[0] == "breed":
        return -1
    return m.repeater_phrase
