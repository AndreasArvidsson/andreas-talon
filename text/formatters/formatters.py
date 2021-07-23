from talon import Module, Context, actions, imgui
import logging
import re

ctx = Context()

formatters_dict = {
    "NOOP": lambda text: text,
    "ALL_CAPS": lambda text: text.upper(),
    "ALL_LOWERCASE": lambda text: text.lower(),
    "DOUBLE_QUOTED_STRING": lambda text: surround(text, '"'),
    "SINGLE_QUOTED_STRING": lambda text: surround(text, "'"),
    # Splitting formatters
    "REMOVE_FORMATTING": lambda text: format_words(text, split, " ", lower, lower),
    "CAPITALIZE_ALL_WORDS": lambda text: format_words(text, split, " ", capitalize, capitalize),
    "CAPITALIZE_FIRST_WORD": lambda text: format_words(text, split, " ", capitalize),
    "CAMEL_CASE": lambda text: format_words(text, split_no_symbols, "", lower, capitalize),
    "PASCAL_CASE": lambda text: format_words(text, split_no_symbols, "", capitalize, capitalize),
    "SNAKE_CASE": lambda text: format_words(text, split_no_symbols, "_", lower, lower),
    "ALL_CAPS_SNAKE_CASE": lambda text: format_words(text, split_no_symbols, "_", upper, upper),
    "DASH_SEPARATED": lambda text: format_words(text, split_no_symbols, "-", lower, lower),
    "DOT_SEPARATED": lambda text: format_words(text, split_no_symbols, ".", lower, lower),
    "SLASH_SEPARATED": lambda text: format_words(text, split_no_symbols, "/", lower, lower),
    "DOUBLE_UNDERSCORE": lambda text: format_words(text, split_no_symbols, "__", lower, lower),
    "DOUBLE_COLON_SEPARATED": lambda text: format_words(text, split_no_symbols, "::", lower, lower),
    "NO_SPACES": lambda text: format_words(text, split_no_symbols, "")
}

# This is the mapping from spoken phrases to formatters
formatters_words = {
    "say": formatters_dict["NOOP"],
    "upper": formatters_dict["ALL_CAPS"],
    "lower": formatters_dict["ALL_LOWERCASE"],
    "string": formatters_dict["DOUBLE_QUOTED_STRING"],
    "twin": formatters_dict["SINGLE_QUOTED_STRING"],
    # Splitting formatters
    "unformat": formatters_dict["REMOVE_FORMATTING"],
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
mod.list("formatters", desc="list of formatters")
ctx.lists["self.formatters"] = formatters_words.keys()


@mod.capture(rule="{self.formatters}+")
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m.formatters_list)


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text("Formatters")
    gui.line()
    for name in sorted(set(formatters_words.keys())):
        gui.text(f"{name.ljust(15)}{actions.user.format_text('one two three', name)}")
    gui.line()
    if gui.button("Hide"):
        actions.user.formatters_hide()


@mod.action_class
class Actions:
    def format_text(text: str, formatters: str) -> str:
        """Formats a text according to formatters. formatters is a comma-separated string of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        result = text
        for fmtr in formatters.split(","):
            result = all_formatters[fmtr](result)
        return result

    def formatted_text(text: str, formatters: str) -> str:
        """Formats a text according to formatters. formatters is a comma-separated string of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        return actions.user.format_text(text, formatters)

    def unformat_text(text: str) -> str:
        """Remove format from text"""
        # Split on delimiters. A delimiter char followed by a blank space is no delimiter.
        text = re.sub(r"[-_.:/](?!\s)+", " ", text)
        # Split camel case. Including numbers
        return actions.user.de_camel(text)

    def formatters_help_toggle():
        """Toggle list all formatters gui"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()


def format_words(text, splitter, delimiter, func_first=None, func_rest=None):
    words = splitter(text)
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


def split(text):
    return text.split()


def split_no_symbols(text):
    return re.sub(r"[^a-zA-Z0-9 ]+", "", text).split()


# Test unformat_text
# tests = {
#     "say": "hello, I'm ip address 2!",
#     "sentence": "Hello, I'm ip address 2!",
#     "allcaps": "HELLO, I'M IP ADDRESS 2!",
#     "camel": "helloThereIPAddressA2a2",
#     "Pascal": "HelloThereIPAddressA2a2",
#     "snake": "hello_there_ip_address_2",
#     "kebab": "hello-there-ip-address-2",
#     "packed": "hello::there::ip::address::2",
#     "dotted": "hello.there.ip.address.2",
#     "slasher": "hello/there/ip/address/2",
#     "dunder": "hello__there__ip_address__2"
# }
# for key, value in tests.items():
#     text = actions.user.unformat_text(value)
#     print(f"{key.ljust(15)}{value.ljust(35)}{text}")
