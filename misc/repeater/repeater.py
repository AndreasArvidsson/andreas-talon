from talon import Module, actions

mod = Module()
last_command = None


@mod.capture(rule="twice | trice | <number_small> times")
def repeater_phrase(m) -> int:
    """Repeater string. Returns an integer for number of times to repeat"""
    if m[0] == "twice":
        return 2
    if m[0] == "trice":
        return 3
    return m.number_small


@mod.capture(rule="<user.repeater_phrase>")
def repeater_phrase_sub_one(m) -> int:
    """Repeater string. Returns an integer for number of times to repeat. Subtracts one"""
    return m.repeater_phrase - 1


@mod.capture(rule="<user.repeater_phrase> | breed")
def repeater_phrase_all(m) -> int:
    """Repeater string. Returns an integer for number of times to repeat, including all"""
    try:
        return m.repeater_phrase
    except AttributeError:
        return -1


@mod.action_class
class Actions:
    def repeat_command(n: int = 1):
        """Repeat the last command n times"""
        global last_command
        if last_command == actions.core.last_command():
            actions.user.debug(f"Blocked repetition of command '{last_command[1]}'")
            return
        last_command = None
        actions.core.repeat_phrase(n)

    def repeat_command_block():
        """Block the repeat of the last command"""
        global last_command
        last_command = actions.core.current_command__unstable()
