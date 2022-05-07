from talon import Module, Context, actions
from ...merge import merge

mod = Module()
ctx = Context()
ctx.matches = r"""
language: en_US
language: sv_SE
"""


# fmt: off

# alphabet = "air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip".split(" ")
alphabet = "air batt cap drum each fine gust harp ink jig kid look made near ox pit quench ram spun trap urn vest whale plex yank zip".split(" ")
default_digits = "zero one two three four five six seven eight nine ten eleven twelve".split(" ")

mod.list("letter", desc="The spoken phonetic alphabet")
ctx.lists["self.letter"] = {
    **{alphabet[i]: chr(ord("a") + i) for i in range(len(alphabet))},
    **{"onyx": "å", "adder": "ä", "earl": "ö"},
}

mod.list("key_number", desc="All number keys")
ctx.lists["self.key_number"] = {default_digits[i]: str(i) for i in range(10)}

mod.list("key_function", desc="All function keys")
ctx.lists["self.key_function"] = {f"F {default_digits[i]}": f"f{i}" for i in range(1, 13)}

mod.list("key_arrow", desc="All arrow keys")
ctx.lists["self.key_arrow"] = {"up", "down", "left", "right"}

mod.list("key_special", desc="All special keys")
ctx.lists["self.key_special"] = merge(
    {
        "enter",
        "tab",
        "delete",
        "backspace",
        "home",
        "end",
        "insert",
        "escape",
        "menu",
        "escape",
    },
    {
        "page up":      "pageup",
        "page down":    "pagedown",
        "print screen": "printscr",
        "caps lock":    "capslock",
        "num lock":     "numlock",
    }
)

mod.list("key_modifier", desc="All modifier keys")
ctx.lists["self.key_modifier"] = {
    "alt":          "alt",
    "control":      "ctrl",
    "shift":        "shift",
    "super":        "super",
}

# Symbols you want available BOTH in dictation and command mode.
mod.list("key_punctuation", desc="Symbols for inserting punctuation into text")
ctx.lists["self.key_punctuation"] = {
    "comma":            ",",
    "period":           ".",
    "colon":            ":",
    "stack":            ":",
    "forward slash":    "/",
    "question mark":    "?",
    "exclamation mark": "!",
}

# Symbols available in command mode, but NOT during dictation.
mod.list("key_symbol", desc="All symbols from the keyboard")
ctx.lists["self.key_symbol"] = {
    "space":            " ",
    "void":             " ",
    "dot":              ".",
    "comma":            ",",
    "stack":            ":",
    "semi":             ";",
    "score":            "_",
    "dash":             "-",

    "minus":            "-",
    "plus":             "+",
    "equal":            "=",
    "caret":            "^",
    "tilde":            "~",
    "bang":             "!",
    "hash":             "#",
    "star":             "*",
    "dollar":           "$",
    "percent":          "%",
    "question":         "?",
    "question mark":    "?",
    "amper":            "&",
    "at sign":          "@",

    "single":           "'",
    "double":           '"',
    "quote":            '"',
    "brick":            "`",

    "slash":            "/",
    "pipe":             "|",
    "pike":             "\\",

    "paren":            "(",
    "raren":            ")",
    "brace":            "{",
    "race":             "}",
    "square":           "[",
    "rare":             "]",
    "angle":            "<",
    "rangle":           ">",
}

# fmt: on

requires_space = {
    "`",
    "^",
    "~",
}


@mod.capture(rule="{self.key_modifier}+")
def key_modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m.key_modifier_list)


@mod.capture(
    rule="{self.letter} | {self.key_number} | {self.key_symbol} | {self.key_special} | {self.key_arrow} | {self.key_function}"
)
def key_unmodified(m) -> str:
    "A single key with no modifiers"
    if m[0] == " ":
        return "space"
    return m[0]


@mod.capture(rule="{self.key_modifier} | <self.key_unmodified>")
def key_any(m) -> str:
    "A single key"
    return m[0]


@mod.capture(rule="spell {self.letter}+")
def spell(m) -> str:
    """Spell word phoneticly"""
    return "".join(m.letter_list)


@mod.capture(rule="{self.letter} | {self.key_number} | {self.key_symbol}")
def any_alphanumeric_key(m) -> str:
    "any alphanumeric key"
    return str(m)


@mod.capture(rule="{self.letter}")
def letter(m) -> str:
    """One letter in the alphabet"""
    return str(m)


@mod.capture(rule="{self.letter}+")
def letters(m) -> str:
    """One or more letters in the alphabet"""
    return "".join(m.letter_list)


# Window specific context

ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""


@ctx_win.action_class("main")
class MainActions:
    def key(key: str):
        actions.next(key)
        if key in requires_space:
            actions.next(" ")
