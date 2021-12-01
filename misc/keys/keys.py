from talon import Module, Context, actions
from ...merge import merge

mod = Module()
ctx = Context()
mod.tag("keys")

# alphabet = "air bat cap drum each fine gust harp sit jury crunch look made near odd pit quench red sun trap urge vest whale plex yank zip".split(" ")
# alphabet = "air bat cap drum each fine gust harp ink jane kid look made near odd pit quench ram soon trap urge vest whale plex yank zip".split(
alphabet = "air bat cap drum each fine gust harp ink jig kid look made near odd pit quench ram soon trap urge vest whale plex yank zip".split(
    " ")
default_digits = "zero one two three four five six seven eight nine ten eleven twelve".split(
    " ")

mod.list("key_alphabet", desc="The spoken phonetic alphabet")
ctx.lists["self.key_alphabet"] = {
    **{alphabet[i]: chr(ord("a") + i) for i in range(len(alphabet))},
    **{"aalder": "å", "aerlig": "ä", "oesten": "ö"}
}

mod.list("key_number", desc="All number keys")
ctx.lists["self.key_number"] = {default_digits[i]: str(i) for i in range(10)}

mod.list("key_function", desc="All function keys")
ctx.lists["self.key_function"] = {
    f"F {default_digits[i]}": f"f{i}" for i in range(1, 13)}

mod.list("key_arrow", desc="All arrow keys")
ctx.lists["self.key_arrow"] = {"up", "down", "left", "right"}

mod.list("key_special", desc="All special keys")
ctx.lists["self.key_special"] = merge(
    {
        "enter", "tab", "delete", "backspace",
        "home", "end", "insert", "escape", "menu"
    },
    {
        "page up":      "pageup",
        "page down":    "pagedown",
        "print screen": "printscr"
    }
)

mod.list("key_modifier", desc="All modifier keys")
ctx.lists["self.key_modifier"] = {
    "alt":          "alt",
    "control":      "ctrl",
    "shift":        "shift",
    "super":        "super"
}

# Symbols you want available BOTH in dictation and command mode.
mod.list("key_punctuation", desc="Symbols for inserting punctuation into text")
ctx.lists["self.key_punctuation"] = {
    "comma":            ",",
    "period":           ".",
    "semicolon":        ";",
    "new line":         "\n",
    "colon":            ":",
    "forward slash":    "/",
    "question mark":    "?",
    "exclamation mark": "!",
    "dollar sign":      "$",
    "asterisk":         "*",
    "hash sign":        "#",
    "number sign":      "#",
    "percent sign":     "%",
    "at sign":          "@",
    "ampersand":        "&"
}

# Symbols available in command mode, but NOT during dictation.
mod.list("key_symbol", desc="All symbols from the keyboard")
ctx.lists["self.key_symbol"] = {
    "void":             " ",
    "dot":              ".",
    "comma":            ",",
    "colon":            ":",
    "semi":             ";",
    "dash":             "-",
    "downscore":        "_",

    "bang":             "!",
    "hash":             "#",
    "star":             "*",
    "dollar":           "$",
    "percent":          "%",
    "question":         "?",
    "amper":            "&",
    "at sign":          "@",

    "quote":            '"',
    "apostrophe":       "'",
    "brick":            "`",

    "slash":            "/",
    "backslash":        "\\",
    "pipe":             "|",

    "paren":            "(",
    "rearen":           ")",
    "brace":            "{",
    "race":             "}",
    "square":           "[",
    "rare":             "]",
    "angle":            "<",
    "rangle":           ">",

    "caret":            "^",
    "tilde":            "~",
    "plus":             "+",
    "minus":            "-",
    "equals":           "="
}

requires_space = {"`", "^", "~"}


@mod.capture(rule="{self.key_modifier}+")
def key_modifiers(m) -> str:
    "One or more modifier keys"
    return "-".join(m.key_modifier_list)


@mod.capture(rule="( {self.key_alphabet} | {self.key_number} | {self.key_symbol} "
              "| {self.key_special} | {self.key_arrow} | {self.key_function} )")
def key_unmodified(m) -> str:
    "A single key with no modifiers"
    return str(m)


@mod.capture(rule="spell {self.key_alphabet}+")
def spell(m) -> str:
    """Spell word phoneticly"""
    return "".join(m.key_alphabet_list)


@mod.capture(rule="({self.key_alphabet} | {self.key_number} | {self.key_symbol})")
def any_alphanumeric_key(m) -> str:
    "any alphanumeric key"
    return str(m).strip()


@mod.capture(rule="{self.key_alphabet}")
def letter(m) -> str:
    """One letter in the alphabet"""
    return str(m)


@mod.capture(rule="{self.key_alphabet}+")
def letters(m) -> str:
    """One or more letters in the alphabet"""
    return "".join(m.key_alphabet_list)


@ctx.action_class("main")
class MainActions:
    def key(key: str):
        actions.next(key)
        if key in requires_space:
            actions.next(" ")
