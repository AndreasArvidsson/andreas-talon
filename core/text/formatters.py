from talon import Module, Context, actions
from dataclasses import dataclass
from typing import Callable, Optional
import re

mod = Module()
ctx = Context()


@dataclass
class Formatter:
    id: str
    format: Callable[[str], str]
    unformat: Optional[Callable[[str], str]] = None


def unformat_upper(text: str) -> str:
    return text.lower() if text.isupper() else text


def unformat_text_for_code(text: str) -> str:
    """Remove format from text"""
    # Don't split delimited sequences in a string with whitespaces.
    # Could for example be: `short-term` or `iPhone` in a sentence
    if re.search(r"\s", text) is None:
        # Split on delimiters.
        result = re.sub(r"[-_.:/]+", " ", text)
        # Split camel case. Including numbers
        result = actions.user.de_camel(result)
        # Delimiter/camel case successfully split. Lower case to restore "original" text.
        if text != result:
            return result.lower()

    return text


formatters = [
    # Simple formatters
    Formatter(
        "NO_FORMAT",
        lambda text: text,
    ),
    Formatter(
        "TRAILING_SPACE",
        lambda text: f"{text} ",
    ),
    Formatter(
        "ALL_UPPERCASE",
        lambda text: text.upper(),
    ),
    Formatter(
        "ALL_LOWERCASE",
        lambda text: text.lower(),
    ),
    Formatter(
        "DOUBLE_QUOTED_STRING",
        lambda text: f'"{text}"',
    ),
    Formatter(
        "SINGLE_QUOTED_STRING",
        lambda text: f"'{text}'",
    ),
    Formatter(
        "NO_SPACES",
        lambda text: re.sub(r"['`\s]", "", text).lower(),
    ),
    # Splitting formatters
    Formatter(
        "CAPITALIZE_FIRST_WORD",
        lambda text: first_and_rest(text, capitalizeSoft),
        unformat_upper,
    ),
    Formatter(
        "CAPITALIZE_ALL_WORDS",
        lambda text: first_and_rest(text, capitalizeSoft, capitalizeSoft),
        unformat_upper,
    ),
    # Delimited formatters
    Formatter(
        "CAMEL_CASE",
        lambda text: format_delim(text, "", lower, capitalize),
        unformat_text_for_code,
    ),
    Formatter(
        "PASCAL_CASE",
        lambda text: format_delim(text, "", capitalize, capitalize),
        unformat_text_for_code,
    ),
    Formatter(
        "SNAKE_CASE",
        lambda text: format_delim(text, "_", lower, lower),
        unformat_text_for_code,
    ),
    Formatter(
        "DASH_SEPARATED",
        lambda text: format_delim(text, "-", lower, lower),
        unformat_text_for_code,
    ),
    Formatter(
        "DOT_SEPARATED",
        lambda text: format_delim(text, ".", lower, lower),
        unformat_text_for_code,
    ),
    Formatter(
        "SLASH_SEPARATED",
        lambda text: format_delim(text, "/", lower, lower),
        unformat_text_for_code,
    ),
    Formatter(
        "DOUBLE_UNDERSCORE",
        lambda text: format_delim(text, "__", lower, lower),
        unformat_text_for_code,
    ),
    Formatter(
        "DOUBLE_COLON_SEPARATED",
        lambda text: format_delim(text, "::", lower, lower),
        unformat_text_for_code,
    ),
    # Re-formatters
    Formatter(
        "REMOVE_FORMATTING",
        lambda text: text.lower(),
        unformat_text_for_code,
    ),
    Formatter(
        "COMMA_SEPARATED",
        lambda text: ", ".join(text.split()),
    ),
]


formatters_dict = {f.id: f for f in formatters}

formatters_code = {
    "smash": "NO_SPACES",
    "camel": "CAMEL_CASE",
    "pascal": "PASCAL_CASE",
    "snake": "SNAKE_CASE",
    "constant": "ALL_UPPERCASE,SNAKE_CASE",
    "kebab": "DASH_SEPARATED",
    "dotted": "DOT_SEPARATED",
    "slasher": "SLASH_SEPARATED",
    # "dunder": "DOUBLE_UNDERSCORE",
    # "packed": "DOUBLE_COLON_SEPARATED",
}

formatters_prose = {
    "sentence": "CAPITALIZE_FIRST_WORD",
    "title": "CAPITALIZE_ALL_WORDS",
    "upper": "ALL_UPPERCASE",
    "lower": "ALL_LOWERCASE",
}


# This is the mapping from spoken phrases to formatters
mod.list("formatter_code", desc="List of code formatters")
ctx.lists["self.formatter_code"] = {
    **formatters_code,
    # I don't want these formatters in the formatter list/capture since they are not for reformatting
    "string": "DOUBLE_QUOTED_STRING",
    # "twin": "SINGLE_QUOTED_STRING",
}

mod.list("formatter_prose", desc="List of prose formatters")
ctx.lists["self.formatter_prose"] = {
    **formatters_prose,
    # I don't want these formatters in the formatter list/capture since they are not for reformatting
    "say": "NO_FORMAT",
}


mod.list("formatter", desc="List of formatters only used for reformatting")
ctx.lists["self.formatter"] = {
    **formatters_code,
    **formatters_prose,
    # These formatters are only for reformatting and neither code or prose
    "list": "COMMA_SEPARATED",
    "un": "REMOVE_FORMATTING",
}

mod.list("formatter_word", desc="List of word formatters")
ctx.lists["self.formatter_word"] = {
    "word": "ALL_LOWERCASE",
    "trot": "TRAILING_SPACE,ALL_LOWERCASE",
    "proud": "CAPITALIZE_FIRST_WORD",
    "leap": "TRAILING_SPACE,CAPITALIZE_FIRST_WORD",
}


@mod.capture(rule="{self.formatter}+")
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m)


@mod.action_class
class Actions:
    def insert_formatted(text: str, formatters: str):
        """Insert text <text> formatted as <formatters>"""
        formatted = actions.user.format_text(text, formatters)
        actions.insert(formatted)

    def format_text(text: str, formatters: str) -> str:
        """Formats <text> as <formatters>"""
        return format_text(text, formatters, unformat=False)

    def reformat_text(text: str, formatters: str) -> str:
        """Re-formats <text> as <formatters>"""
        return format_text(text, formatters, unformat=True)

    def reformat_selection(formatters: str):
        """Reformats the current selection as <formatters>"""
        selected = actions.edit.selected_text()
        if selected:
            formatted = actions.user.reformat_text(selected, formatters)
            actions.insert(formatted)

    def de_camel(text: str) -> str:
        """Replacing camelCase boundaries with blank space"""
        Ll = "a-zåäö"
        Lu = "A-ZÅÄÖ"
        L = f"{Ll}{Lu}"
        low_to_upper = rf"(?<=[{Ll}])(?=[{Lu}])"  # camel|Case
        upper_to_last_upper = rf"(?<=[L{Lu}])(?=[{Lu}][{Ll}])"  # IP|Address
        letter_to_digit = rf"(?<=[{L}])(?=[\d])"  # version|10
        digit_to_letter = rf"(?<=[\d])(?=[{L}])"  # 2|x
        return re.sub(
            rf"{low_to_upper}|{upper_to_last_upper}|{letter_to_digit}|{digit_to_letter}",
            " ",
            text,
        )


def format_text(text: str, formatters: str, unformat: bool) -> str:
    """Formats a text according to formatters. formatters is a comma-separated string of formatters (e.g. 'CAPITALIZE_ALL_WORDS,SNAKE_CASE')"""
    text, pre, post = shrink_to_string_inside(text)

    for i, formatter_name in enumerate(reversed(formatters.split(","))):
        formatter = formatters_dict[formatter_name]
        if unformat and i == 0 and formatter.unformat:
            text = formatter.unformat(text)
        text = formatter.format(text)

    return f"{pre}{text}{post}"


def format_delim(
    text,
    delimiter,
    format_first=None,
    format_rest=None,
):
    # Strip anything that is not alpha-num, whitespace or dot
    text = re.sub(r"[^\w\d\s.]+", "", text)
    # Split on anything that is not alpha-num
    words = re.split(r"([^\w\d]+)", text)
    groups = []
    group = []
    first = True

    for word in words:
        if word.isspace():
            continue
        # Word is number
        if bool(re.match(r"\d+", word)):
            first = True
        # Word is symbol
        elif bool(re.match(r"\W+", word)):
            groups.append(delimiter.join(group))
            word = word.strip()
            first = True
            groups.append(word)
            group = []
            continue
        elif first:
            first = False
            if format_first:
                word = format_first(word)
        elif format_rest:
            word = format_rest(word)
        group.append(word)

    groups.append(delimiter.join(group))
    return "".join(groups)


def first_and_rest(text, format_first=None, format_rest=None):
    words = [x for x in re.split(r"(\s+)", text) if x]
    first = True

    for i, word in enumerate(words):
        if word.isspace():
            continue
        if first:
            first = False
            if format_first:
                words[i] = format_first(word)
        elif format_rest:
            words[i] = format_rest(word)

    return "".join(words)


string_delimiters = [
    ['"""', '"""'],
    ['"', '"'],
    ["'", "'"],
]


def shrink_to_string_inside(text: str) -> (str, str, str):
    for [left, right] in string_delimiters:
        if text.startswith(left) and text.endswith(right):
            return text[len(left) : -len(right)], left, right
    return text, "", ""


def capitalizeSoft(text: str) -> str:
    return f"{text[0].upper()}{text[1:]}"


def capitalize(text: str) -> str:
    return text.capitalize()


def lower(text: str) -> str:
    return text.lower()


def upper(text: str) -> str:
    return text.upper()
