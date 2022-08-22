from talon import Module, Context, ui, actions, grammar
import re

mod = Module()

ctx = Context()
ctx.matches = r"""
language: en
language: sv
"""


# ----- Captures used in both command and dictation mode -----


@mod.capture(rule="{user.vocabulary} | <word>")
def word(m) -> str:
    """A single word, including user-defined vocabulary."""
    words = capture_to_words(m)
    return words[0].replace(" ", "")


# Used to escape numbers and symbols
@mod.capture(rule="({user.vocabulary} | <phrase>)+")
def words(m) -> str:
    """A sequence of words, including user-defined vocabulary."""
    return format_phrase(m)


@mod.capture(rule="{self.letter} {self.letter}+")
def spell(m) -> str:
    """Spell word phoneticly"""
    return "".join(m.letter_list)


@mod.capture(rule="blah")
def placeholder(m) -> str:
    """Placeholder word"""
    return "PLACEHOLDER"


text_rule_parts = [
    "{user.vocabulary}",
    "{user.key_punctuation}",
    "<user.abbreviation>",
    "<user.spell>",
    # "<user.number_dd>",
    "<user.number_prefix>",
    "<phrase>",
]

prose_rule_parts = [
    "{user.vocabulary}",
    "{user.key_punctuation}",
    "<user.abbreviation>",
    "<user.spell>",
    # "<user.number_dd>",
    "<user.number_prefix>",
    "<user.placeholder>",
    "<phrase>",
]

text_rule = f"({'|'.join(text_rule_parts)})+"
code_rule = text_rule.replace("{user.key_punctuation}", "{user.key_punctuation_code}")
prose_role = f"({'|'.join(prose_rule_parts)})+"


@mod.capture(rule=text_rule)
def text(m) -> str:
    """Mixed words, numbers and punctuation, including user-defined vocabulary, abbreviations and spelling."""
    return format_phrase(m)


@mod.capture(rule=code_rule)
def text_code(m) -> str:
    """Same as <user.text>, but with fewer punctuations"""
    return format_phrase(m)


@mod.capture
def prose() -> str:
    """Same as <user.text>, but auto-spaced & capitalized."""


# The prose capture needs to be defined on the context to work with Swedish dictation.
@ctx.capture("user.prose", rule=prose_role)
def prose(m) -> str:
    text, _state = auto_capitalize(format_phrase(m))
    return text


# ----- Dictation mode only -----

ctx_dictation = Context()
ctx_dictation.matches = r"""
mode: dictation
language: en
language: sv
"""


@ctx_dictation.action_class("main")
class main_action:
    def auto_insert(text):
        actions.user.dictation_insert(text)


# ---------- FORMATTING ---------- #
def format_phrase(m):
    words = capture_to_words(m)
    result = ""
    for i, word in enumerate(words):
        if i > 0 and needs_space_between(words[i - 1], word):
            result += " "
        result += word
    return result


def capture_to_words(m):
    words = []
    for item in m:
        words.extend(
            actions.dictate.replace_words(actions.dictate.parse_words(item))
            if isinstance(item, grammar.vm.Phrase)
            else [item]
        )
    words = actions.user.homophones_replace_words(words)
    return words


# There must be a simpler way to do this, but I don't see it right now.
no_space_after = re.compile(
    r"""
  (?:
    [\s\-_/#@([{‘“]     # characters that never need space after them
  | (?<!\w)[$£€¥₩₽₹]    # currency symbols not preceded by a word character
  # quotes preceded by beginning of string, space, opening braces, dash, or other quotes
  | (?: ^ | [\s([{\-'"] ) ['"]
  )$""",
    re.VERBOSE,
)
no_space_before = re.compile(
    r"""
  ^(?:
    [\s\-_.,!?;:/%)\]}’”]   # characters that never need space before them
  | [$£€¥₩₽₹](?!\w)         # currency symbols not followed by a word character
  # quotes followed by end of string, space, closing braces, dash, other quotes, or some punctuation.
  | ['"] (?: $ | [\s)\]}\-'".,!?;:/] )
  )""",
    re.VERBOSE,
)


def omit_space_before(text: str) -> bool:
    return not text or no_space_before.search(text)


def omit_space_after(text: str) -> bool:
    return not text or no_space_after.search(text)


def needs_space_between(before: str, after: str) -> bool:
    return not (omit_space_after(before) or omit_space_before(after))


# # TESTS, uncomment to enable
# assert needs_space_between("a", "break")
# assert needs_space_between("break", "a")
# assert needs_space_between(".", "a")
# assert needs_space_between("said", "'hello")
# assert needs_space_between("hello'", "said")
# assert needs_space_between("hello.", "'John")
# assert needs_space_between("John.'", "They")
# assert needs_space_between("paid", "$50")
# assert needs_space_between("50$", "payment")
# assert not needs_space_between("", "")
# assert not needs_space_between("a", "")
# assert not needs_space_between("a", " ")
# assert not needs_space_between("", "a")
# assert not needs_space_between(" ", "a")
# assert not needs_space_between("a", ",")
# assert not needs_space_between("'", "a")
# assert not needs_space_between("a", "'")
# assert not needs_space_between("and-", "or")
# assert not needs_space_between("mary", "-kate")
# assert not needs_space_between("$", "50")
# assert not needs_space_between("US", "$")
# assert not needs_space_between("(", ")")
# assert not needs_space_between("(", "e.g.")
# assert not needs_space_between("example", ")")
# assert not needs_space_between("example", '".')
# assert not needs_space_between("example", '."')
# assert not needs_space_between("hello'", ".")
# assert not needs_space_between("hello.", "'")


def auto_capitalize(text, state=None):
    """
    Auto-capitalizes text. `state` argument means:
    - None: Don't capitalize initial word.
    - "sentence start": Capitalize initial word.
    - "after newline": Don't capitalize initial word, but we're after a newline.
      Used for double-newline detection.
    Returns (capitalized text, updated state).
    """
    output = ""
    # Imagine a metaphorical "capitalization charge" travelling through the
    # string left-to-right.
    charge = state == "sentence start"
    newline = state == "after newline"
    for c in text:
        # Sentence endings & double newlines create a charge.
        if c in ".!?" or (newline and c == "\n"):
            charge = True
        # Alphanumeric characters and commas/colons absorb charge & try to
        # capitalize (for numbers & punctuation this does nothing, which is what
        # we want).
        elif charge and (c.isalnum() or c in ",:"):
            charge = False
            c = c.capitalize()
        # Otherwise the charge just passes through.
        output += c
        newline = c == "\n"
    return output, (
        "sentence start" if charge else "after newline" if newline else None
    )


# ---------- DICTATION AUTO FORMATTING ---------- #
class DictationFormat:
    def __init__(self):
        self.reset()

    def reset(self):
        self.before = ""
        self.state = "sentence start"

    def update_context(self, before):
        if before is None:
            return
        self.reset()
        self.pass_through(before)

    def pass_through(self, text):
        _, self.state = auto_capitalize(text, self.state)
        self.before = text or self.before

    def format(self, text):
        if needs_space_between(self.before, text):
            text = " " + text
        text, self.state = auto_capitalize(text, self.state)
        self.before = text or self.before
        return text


dictation_formatter = DictationFormat()
ui.register("app_deactivate", lambda app: dictation_formatter.reset())
ui.register("win_focus", lambda win: dictation_formatter.reset())


@mod.action_class
class Actions:
    def dictation_format_reset():
        """Resets the dictation formatter"""
        return dictation_formatter.reset()

    def dictation_insert(text: str) -> str:
        """Inserts dictated text, formatted appropriately."""
        before, after = actions.user.dictation_get_context()

        if (
            not omit_space_before(text)
            or text != auto_capitalize(text, "sentence start")[0]
        ):
            dictation_formatter.update_context(before)

        add_space_after = not omit_space_after(text) and needs_space_between(
            text, after
        )

        text = dictation_formatter.format(text)

        if add_space_after:
            text += " "

        actions.insert(text)

        if add_space_after:
            actions.edit.left()

    def dictation_get_context() -> tuple[str, str]:
        """Returns the text before and after the current selection"""
        return (None, None)
