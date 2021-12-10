from talon import Module

mod = Module()


@mod.capture(rule="twice | trice | <number_small> times")
def repeater_phrase(m) -> int:
    """Parser repeater string and returns an integer for number of times to repeat"""
    if m[0] == "twice":
        return 1
    if m[0] == "trice":
        return 2
    return m.number_small - 1
