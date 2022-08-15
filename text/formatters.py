from talon import Module, Context, actions
import re
from ..imgui import imgui

mod = Module()
ctx = Context()

mod.mode("help_formatters", "Mode for showing the formatter help gui")

formatters_dict = {
    # Simple formatters
    "NOOP": lambda text: text,
    "TRAILING_PADDING": lambda text: f"{text} ",
    "ALL_CAPS": lambda text: text.upper(),
    "ALL_LOWERCASE": lambda text: text.lower(),
    "DOUBLE_QUOTED_STRING": lambda text: f'"{text}"',
    "SINGLE_QUOTED_STRING": lambda text: f"'{text}'",
    # Splitting formatters
    "CAPITALIZE_ALL_WORDS": lambda text: first_and_rest(text, capitalize, capitalize),
    "CAPITALIZE_FIRST_WORD": lambda text: first_and_rest(text, capitalize),
    # Delimited formatters
    "CAMEL_CASE": lambda text: format_delim(text, "", lower, capitalize),
    "PASCAL_CASE": lambda text: format_delim(text, "", capitalize, capitalize),
    "SNAKE_CASE": lambda text: format_delim(text, "_", lower, lower),
    "ALL_CAPS_SNAKE_CASE": lambda text: format_delim(text, "_", upper, upper),
    "DASH_SEPARATED": lambda text: format_delim(text, "-", lower, lower),
    "DOT_SEPARATED": lambda text: format_delim(text, ".", lower, lower),
    "SLASH_SEPARATED": lambda text: format_delim(text, "/", lower, lower),
    "DOUBLE_UNDERSCORE": lambda text: format_delim(text, "__", lower, lower),
    "DOUBLE_COLON_SEPARATED": lambda text: format_delim(text, "::", lower, lower),
    "NO_SPACES": lambda text: format_delim(text, ""),
    # Re formatters
    "REMOVE_FORMATTING": lambda text: text.lower(),
    "COMMA_SEPARATED": lambda text: ", ".join(text.split()),
}

formatters_no_unformat = {
    "ALL_CAPS",
    "ALL_LOWERCASE",
    "DOUBLE_QUOTED_STRING",
    "SINGLE_QUOTED_STRING",
    "COMMA_SEPARATED",
}

# This is the mapping from spoken phrases to formatters
mod.list("formatter_code", desc="List of code formatters")
ctx.lists["self.formatter_code"] = {
    "upper": "ALL_CAPS",
    "lower": "ALL_LOWERCASE",
    "string": "DOUBLE_QUOTED_STRING",
    "twin": "SINGLE_QUOTED_STRING",
    # Splitting formatters
    "title": "CAPITALIZE_ALL_WORDS",
    "camel": "CAMEL_CASE",
    "pascal": "PASCAL_CASE",
    "snake": "SNAKE_CASE",
    "constant": "ALL_CAPS_SNAKE_CASE",
    "kebab": "DASH_SEPARATED",
    "dotted": "DOT_SEPARATED",
    "slasher": "SLASH_SEPARATED",
    "dunder": "DOUBLE_UNDERSCORE",
    "packed": "DOUBLE_COLON_SEPARATED",
    "smash": "NO_SPACES",
}

mod.list("formatter_prose", desc="List of prose formatters")
ctx.lists["self.formatter_prose"] = {
    "say": "NOOP",
    "sentence": "CAPITALIZE_FIRST_WORD",
    "string sentence": "DOUBLE_QUOTED_STRING,CAPITALIZE_FIRST_WORD",
    "twin sentence": "SINGLE_QUOTED_STRING,CAPITALIZE_FIRST_WORD",
}


mod.list("formatter_word", desc="List of word formatters")
ctx.lists["self.formatter_word"] = {
    "word": "ALL_LOWERCASE",
    "trot": "TRAILING_PADDING,ALL_LOWERCASE",
    "proud": "CAPITALIZE_FIRST_WORD",
    "leap": "TRAILING_PADDING,CAPITALIZE_FIRST_WORD",
}

mod.list(
    "formatter_hidden", desc="List of hidden formatters. Are only used for reformat"
)
ctx.lists["self.formatter_hidden"] = {
    "list": "COMMA_SEPARATED",
    "un": "REMOVE_FORMATTING",
}


mod.list("phrase_ender", desc="List of commands that can be used to end a phrase")
ctx.lists["self.phrase_ender"] = {
    "void": " ",
    "slap": "\n",
    "over": "",
}


@mod.capture(rule="{self.formatter_code}+")
def formatters_code(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'DOUBLE_QUOTED_STRING,CAPITALIZE_FIRST_WORD'"
    return ",".join(m.formatter_code_list)


@mod.capture(
    rule="({self.formatter_code} | {self.formatter_prose} | {self.formatter_hidden})+"
)
def formatters(m) -> str:
    "Returns a comma-separated string of formatters e.g. 'SNAKE,DUBSTRING'"
    return ",".join(m)


@imgui.open()
def gui(gui: imgui.GUI):
    gui.header("Formatters")
    gui.line(bold=True)
    formatters = {
        **ctx.lists["self.formatter_code"],
        **ctx.lists["self.formatter_prose"],
    }
    for name in sorted(set(formatters)):
        gui.text(
            f"{name.ljust(30)}{actions.user.format_text('one two three', formatters[name])}"
        )
    gui.spacer()
    if gui.button("Hide"):
        actions.user.formatters_help_toggle()


@mod.action_class
class Actions:
    def insert_formatted(text: str, formatters: str):
        """Inserts a text formatted according to formatters. Formatters is a comma separated list of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        formatted = actions.user.format_text(text, formatters)
        actions.insert(formatted)

    def format_text(text: str, formatters: str) -> str:
        """Formats a text according to formatters. formatters is a comma-separated string of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        for fmtr in reversed(formatters.split(",")):
            text = formatters_dict[fmtr](text)
        return text

    def reformat_text(text: str, formatters: str) -> str:
        """Reformat the text. Used by Cursorless"""
        lines = text.split("\n")
        for i in range(len(lines)):
            unformatted = actions.user.unformat_text(lines[i], formatters)
            lines[i] = actions.user.format_text(unformatted, formatters)
        return "\n".join(lines)

    def reformat_selection(formatters: str):
        """Reformats the current selection."""
        selected = actions.edit.selected_text()
        if not selected:
            return
        formatted = actions.user.reformat_text(selected, formatters)
        actions.insert(formatted)

    def unformat_text(text: str, formatters: str = None) -> str:
        """Remove format from text"""
        # Some formatters don't use unformat before
        if formatters in formatters_no_unformat:
            return text
        # Remove quotes
        text = de_string(text)
        # Split on delimiters. A delimiter char followed by a blank space is no delimiter.
        result = re.sub(r"[-_.:/](?!\s)+", " ", text)
        # Split camel case. Including numbers
        result = actions.user.de_camel(result)
        # Delimiter/camel case successfully split. Lower case to restore "original" text.
        if text != result:
            result = result.lower()
        return result

    def de_camel(text: str) -> str:
        """Replacing camelCase boundaries with blank space"""
        return re.sub(
            r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])",
            " ",
            text,
        )

    def formatters_help_toggle():
        """Toggle list all formatters gui"""
        if gui.showing:
            actions.mode.disable("user.help_formatters")
            gui.hide()
        else:
            gui.show()
            actions.mode.enable("user.help_formatters")


def format_delim(
    text,
    delimiter,
    format_first=None,
    format_rest=None,
):
    # Strip apostrophes and quotes
    text = re.sub(r"['`\"]+", "", text)
    # Split on anything that is not alpha-num
    words = re.split(r"([^a-zA-Z0-9]+)", text)
    groups = []
    group = []
    first = True

    for word in words:
        if not word.strip():
            continue
        # Word is number
        if bool(re.match(r"\d+", word)):
            first = True
        # Word is symbol
        elif bool(re.match(r"[^a-zA-Z]+", word)):
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
    words = text.split()
    for i, word in enumerate(words):
        if i == 0:
            if format_first:
                words[i] = format_first(word)
        elif format_rest:
            words[i] = format_rest(word)
    return " ".join(words)


def capitalize(text: str) -> str:
    return text.lower().capitalize()


def lower(text: str) -> str:
    return text.lower()


def upper(text: str) -> str:
    return text.upper()


def de_string(text: str) -> str:
    return text.strip('"').strip("'")
