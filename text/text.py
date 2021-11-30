from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def insert_string(text: str):
        """Inserts the string"""
        insert_string(text, text)

    def insert_and_format(text: str, formatters: str):
        """Inserts a text formatted according to formatters. Formatters is a comma separated list of formatters (e.g. 'CAPITALIZE_ALL_WORDS,DOUBLE_QUOTED_STRING')"""
        formatted = actions.user.format_text(text, formatters)
        insert_string(formatted, text)

    def reformat_last(formatters: str):
        """Clears and reformats last formatted phrase"""
        last_phrase = actions.user.history_get_last_phrase()
        if not last_phrase:
            return
        last_unformatted = actions.user.history_get_last_unformatted()
        actions.user.history_clear_last_phrase()
        if last_unformatted:
            actions.user.insert_and_format(last_unformatted, formatters)
        else:
            actions.user.insert_and_format(last_phrase, formatters)

    def reformat_selection(formatters: str):
        """Reformats the current selection."""
        selected = actions.edit.selected_text()
        if not selected:
            return
        selections = selected.split("\n")
        if len(selections) == 1:
            reformat_single_selection(selections[0], formatters)
        else:
            reformat_multiple_selections(selections, formatters)

    def reformat_text(text: str, formatters: str) -> str:
        """Reformat the text. Used by Cursorless"""
        lines = text.split("\n")
        for i in range(len(lines)):
            unformatted = actions.user.unformat_text(lines[i], formatters)
            lines[i] = actions.user.format_text(unformatted, formatters)
        return "\n".join(lines)


def reformat_single_selection(selected: str, formatters: str):
    unformatted = actions.user.unformat_text(selected, formatters)
    formatted = actions.user.format_text(unformatted, formatters)
    insert_string(formatted, unformatted)


def reformat_multiple_selections(selections: list[str], formatters: str):
    actions.user.homophones_hide()
    formatted_parts = []
    for selected in selections:
        unformatted = actions.user.unformat_text(selected, formatters)
        formatted = actions.user.format_text(unformatted, formatters)
        actions.user.history_add_phrase(formatted, unformatted)
        formatted_parts.append(formatted)
    formatted_all = "\n".join(formatted_parts)
    actions.insert(formatted_all)


def insert_string(formatted: str, unformatted: str):
    actions.user.homophones_hide()
    actions.insert(formatted)
    actions.user.history_add_phrase(formatted, unformatted)
