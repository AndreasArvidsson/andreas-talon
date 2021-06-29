from talon import Module, Context, actions, imgui
import logging
import re
from user.util import de_camel

ctx = Context()

formatters_dict = {
    "NOOP": lambda text: text,
    "ALL_CAPS": lambda text: text.upper(),
    "ALL_LOWERCASE": lambda text: text.lower(),
    "DOUBLE_QUOTED_STRING": lambda text: surround(text, '"'),
    "SINGLE_QUOTED_STRING": lambda text: surround(text, "'"),
    # Splitting formatters
    "CAPITALIZE_ALL_WORDS": lambda text: format_words(text, " ", capitalize, capitalize),
    "CAPITALIZE_FIRST_WORD": lambda text: format_words(text, " ", capitalize),
    "CAMEL_CASE": lambda text: format_words(text, "", lower, capitalize),
    "PASCAL_CASE": lambda text: format_words(text, "", capitalize, capitalize),
    "SNAKE_CASE": lambda text: format_words(text, "_", lower, lower),
    "ALL_CAPS_SNAKE_CASE": lambda text: format_words(text, "_", upper, upper),
    "DASH_SEPARATED": lambda text: format_words(text, "-", lower, lower),
    "DOT_SEPARATED": lambda text: format_words(text, ".", lower, lower),
    "SLASH_SEPARATED": lambda text: format_words(text, "/", lower, lower),
    "DOUBLE_UNDERSCORE": lambda text: format_words(text, "__", lower, lower),
    "DOUBLE_COLON_SEPARATED": lambda text: format_words(text, "::", lower, lower),
    "NO_SPACES": lambda text: format_words(text, "")
}

# This is the mapping from spoken phrases to formatters
formatters_words = {
    "say": formatters_dict["NOOP"],
    "allcaps": formatters_dict["ALL_CAPS"],
    "alldown": formatters_dict["ALL_LOWERCASE"],
    "string": formatters_dict["DOUBLE_QUOTED_STRING"],
    "twin": formatters_dict["SINGLE_QUOTED_STRING"],
    # Splitting formatters
    "title": formatters_dict["CAPITALIZE_ALL_WORDS"],
    "sentence": formatters_dict["CAPITALIZE_FIRST_WORD"],
    "camel": formatters_dict["CAMEL_CASE"],
    "pascal": formatters_dict["PASCAL_CASE"],
    "snake": formatters_dict["SNAKE_CASE"],
    "constant": formatters_dict["ALL_CAPS_SNAKE_CASE"],
    "kebab": formatters_dict["DASH_SEPARATED"],
    "dotted": formatters_dict["DOT_SEPARATED"],
    "slasher": formatters_dict["SLASH_SEPARATED"],
    "dunder": formatters_dict["DOUBLE_UNDERSCORE"],
    "packed": formatters_dict["DOUBLE_COLON_SEPARATED"],
    "smash": formatters_dict["NO_SPACES"]
}

all_formatters = {}
all_formatters.update(formatters_dict)
all_formatters.update(formatters_words)

mod = Module()
mod.mode("formatters")
mod.list("formatters", desc="list of formatters")
ctx.lists["self.formatters"] = formatters_words.keys()


@mod.capture(rule="{self.formatters}+")
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m.formatters_list)


@mod.capture(rule="<self.formatters> <user.text> (<user.text> | <user.formatter_immune>)*")
def format_text(m) -> str:
    "Formats the text and returns a string"
    formatters = m[0]
    text = ""
    for chunk in m[1:]:
        if isinstance(chunk, ImmuneString):
            text += chunk.string + " "
        else:
            text += chunk
    return format_phrase(text, formatters)


class ImmuneString(object):
    """Wrapper that makes a string immune from formatting."""

    def __init__(self, string):
        self.string = string


@mod.capture(rule="{user.key_symbol}")
def formatter_immune(m) -> ImmuneString:
    """Text that can be interspersed into a formatter, e.g. characters. It will be inserted directly, without being formatted."""
    return ImmuneString(str(m))


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Formatters")
    gui.line()
    for name in sorted(set(formatters_words.keys())):
        gui.text(f"{name.ljust(15)}{format_phrase('one two three', name)}")
    gui.line()
    if gui.button("Hide"):
        actions.user.formatters_hide()


@mod.action_class
class Actions:
    def formatted_text(phrase: str, formatters: str) -> str:
        """Formats a phrase according to formatters. formatters is a comma-separated string of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        return format_phrase(phrase, formatters)

    def formatters_help_toggle():
        """Lists all formatters"""
        if gui.showing:
            actions.user.formatters_hide()
        else:
            actions.mode.enable("user.formatters")
            gui.show()

    def formatters_hide():
        """Hide formatters"""
        actions.mode.disable("user.formatters")
        gui.hide()

    def insert_string(text: str):
        """Inserts the string"""
        actions.insert(text)
        actions.user.history_add_phrase(text)
        actions.user.alternatives_last(text)

    def insert_formatted(phrase: str, formatters: str):
        """Inserts a phrase formatted according to formatters. Formatters is a comma separated list of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        phrase = format_phrase(phrase, formatters)
        actions.user.insert_string(phrase)

    def formatters_reformat_last(formatters: str) -> str:
        """Clears and reformats last formatted phrase"""
        last_phrase = actions.user.history_get_last_phrase()
        if last_phrase:
            actions.user.history_clear_last_phrase()
            actions.user.insert_formatted(last_phrase, formatters)

    def formatters_reformat_selection(formatters: str) -> str:
        """Reformats the current selection."""
        selected = actions.edit.selected_text()
        if not selected:
            return
        text = actions.self.formatted_text(selected, formatters)
        if selected == text:
            return
        actions.user.insert_string(text)




def format_phrase(phrase: str, fmtrs: str):
    result = phrase
    for fmtr in fmtrs.split(","):
        result = all_formatters[fmtr](result)
    return result


def format_words(text: str, delimiter: str, func_first=None, func_rest=None):
    words = split_words(text)
    result = []
    for i, word in enumerate(words):
        if i == 0:
            if func_first:
                word = func_first(word)
        elif func_rest:
            word = func_rest(word)
        result.append(word)
    return delimiter.join(result)


def capitalize(text): return text.lower().capitalize()
def lower(text): return text.lower()
def upper(text): return text.upper()

def surround(text, char):
    if text[0] == "'" or text[0] == '"':
        text = text[1:]
    length = len(text)
    if text[-1] == "'" or text[-1] == '"':
        text = text[:-1]
    return char + text + char

def split_words(text):
    # Split on delimiters. A delimiter char followed by a blank space is no delimiter.
    text = re.sub(r"[-_.:/](?!\s)+", " ", text)
    # Split camel case. Including numbers
    text = de_camel(text)
    return text.split()

# Test split_words
# tests = {
#     "say": "hello, I'm ip address 2!",
#     "sentence": "Hello, I'm ip address 2!",
#     "allcaps": "HELLO, I'M IP ADDRESS 2!",
#     "camel": "helloThereIPAddressA2a2",
#     "Pascal": "HelloThereIPAddressA2a2",
#     "snake":"hello_there_ip_address_2",
#     "kebab":"hello-there-ip-address-2",
#     "packed":"hello::there::ip::address::2",
#     "dotted":"hello.there.ip.address.2",
#     "slasher":"hello/there/ip/address/2",
#     "dunder":"hello__there__ip_address__2"
# }
# for key, value in tests.items():
#     words = split_words(value)
#     text = " ".join(words)
#     print(f"{key.ljust(15)}{value.ljust(35)}{text}")
