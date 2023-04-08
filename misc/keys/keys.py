from talon import Module, Context, actions
import re
from ...merge import merge

mod = Module()

ctx_en = Context()

ctx_sv = Context()
ctx_sv.matches = r"""
language: sv
"""


# fmt: off

default_digits = "zero one two three four five six seven eight nine ten eleven twelve".split(" ")

mod.list("letter", desc="The spoken phonetic alphabet")

mod.list("digit", desc="All number/digit keys")
ctx_en.lists["self.digit"] = {default_digits[i]: str(i) for i in range(10)}

mod.list("key_function", desc="All function keys")
ctx_en.lists["self.key_function"] = {f"F {default_digits[i]}": f"f{i}" for i in range(1, 13)}

mod.list("key_arrow", desc="All arrow keys")
ctx_en.lists["self.key_arrow"] = {"up", "down", "left", "right"}

mod.list("key_special", desc="All special keys")
ctx_en.lists["self.key_special"] = merge(
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
    },
    {
        "deli":         "delete",
        "page up":      "pageup",
        "page down":    "pagedown",
        "print screen": "printscr",
        "caps lock":    "capslock",
        "num lock":     "numlock",
    }
)

mod.list("key_modifier", desc="All modifier keys")
ctx_en.lists["self.key_modifier"] = {
    "alt":          "alt",
    "control":      "ctrl",
    "shift":        "shift",
    "super":        "super",
}

# Symbols you want available BOTH in dictation and command mode.
mod.list("key_punctuation", desc="Symbols for inserting punctuation into text")
ctx_en.lists["self.key_punctuation"] = {
    "period":           ".",
    "comma":            ",",
    "colon":            ":",
    "slash":            "/",
    "forward slash":    "/",
    "question mark":    "?",
    "exclamation mark": "!",
}
ctx_sv.lists["self.key_punctuation"] = {
    "punkt":            ".",
    "kommatecken":      ",",
    "kolon":            ":",
    "snedstreck":       "/",
    "frågetecken":      "?",
    "utropstecken":     "!",

    # For vosk engine
    "\\Punkt":          ".",
    "komma tecken":     ",",
    # "kolon":          ":",
    "snedsträck":       "/",
    "\\Frågetecken":    "?",
    "\\Utropstecken":   "!",
}

# Symbols you want available ONLY in code formatters.
mod.list("key_punctuation_code", desc="Symbols for inserting punctuation into code formatters")
ctx_en.lists["self.key_punctuation_code"] = {
    "dot":           ".",
}

# Symbols available in command mode, but NOT during dictation.
mod.list("symbol", desc="All symbols from the keyboard")

# fmt: on


@mod.capture(rule="{self.key_modifier}+")
def key_modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m)


@mod.capture(
    rule="{self.letter} | {self.digit} | {self.symbol} | {self.key_special} | {self.key_arrow} | {self.key_function}"
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


@mod.capture(rule="{self.letter} | {self.digit} | {self.symbol}")
def any_alphanumeric_key(m) -> str:
    "A single alphanumeric key"
    if m[0] == " ":
        return "space"
    return m[0]


@mod.capture(rule="<user.any_alphanumeric_key>+")
def any_alphanumeric_keys(m) -> str:
    "One or more alphanumeric keys. Space separated"
    return " ".join(m)


@mod.capture(rule="{self.letter}")
def letter(m) -> str:
    """One letter in the alphabet"""
    return m[0]


@mod.capture(rule="{self.letter}+")
def letters(m) -> str:
    """One or more letters in the alphabet"""
    return "".join(m)


# Window specific context

ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""

KEY_REPLACEMENT_RE = re.compile(r"([`^~])")


@ctx_win.action_class("main")
class MainActions:
    def key(key: str):
        actions.next(
            KEY_REPLACEMENT_RE.sub(r"\1 space", key),
        )
