from dataclasses import dataclass
from typing import Callable, Union
from talon import Module, actions


@dataclass
class EditSimpleAction:
    type: str


@dataclass
class EditInsertAction:
    type = "insert"
    text: str


@dataclass
class EditWrapAction:
    type = "wrapWithPairedDelimiter"
    pair: str


@dataclass
class EditFormatAction:
    type = "applyFormatter"
    formatters: str


EditAction = Union[
    EditSimpleAction,
    EditInsertAction,
    EditWrapAction,
    EditFormatAction,
]


mod = Module()
mod.list("edit_simple_action", desc="Actions for the edit command")
mod.list("edit_scope_type", desc="Scope types for the edit command")


@mod.capture(rule="{user.edit_simple_action}")
def edit_simple_action(m) -> EditSimpleAction:
    return EditSimpleAction(m.edit_simple_action)


@mod.capture(rule="{user.delimiter_pair_wrap} wrap")
def edit_wrap_action(m) -> EditWrapAction:
    return EditWrapAction(m.delimiter_pair_wrap)


@mod.capture(rule="<user.formatters> (format | form)")
def edit_format_action(m) -> EditFormatAction:
    return EditFormatAction(m.formatters)


@mod.capture(
    rule="<user.edit_simple_action>"
    " | <user.edit_wrap_action>"
    " | <user.edit_format_action>"
)
def edit_action(m) -> EditAction:
    return m[0]


@mod.capture(rule="{user.edit_scope_type}")
def edit_modifier_containing_scope(m) -> dict:
    return {
        "type": "containingScope",
        "scopeType": m.edit_scope_type,
    }


@mod.capture(rule="this")
def edit_modifier_this(m) -> dict:
    return {
        "type": "containingTokenIfEmpty",
    }


@mod.capture(rule="head | tail")
def edit_modifier_head_tail(m) -> dict:
    return {
        "type": "extendThroughStartOf" if m[0] == "head" else "extendThroughEndOf",
    }


@mod.capture(
    rule="<user.edit_modifier_containing_scope> | "
    "<user.edit_modifier_this> | "
    "<user.edit_modifier_head_tail>"
)
def edit_modifier(m) -> dict:
    return m[0]


@mod.action_class
class Actions:
    def edit_command(action: EditAction, modifiers: list[dict]):
        """Perform edit command"""

        if run_compound_action(action, modifiers):
            return

        try:
            action_callback = get_action_callback(action)
            modifier_callbacks = get_modifier_callbacks(modifiers)
            for callback in reversed(modifier_callbacks):
                callback()
            return action_callback()
        except ValueError as ex:
            actions.app.notify(str(ex))


def run_compound_action(action: EditAction, modifiers: list[dict]):
    if len(modifiers) != 1:
        return False

    action_type = action.type
    modifier = modifiers[0]

    if modifier["type"] != "containingScope":
        return False

    scope_type = modifier["scopeType"]

    if action_type == "setSelection":
        match scope_type:
            case "selection":
                actions.skip()
            case "token":
                actions.edit.select_word()
            case "line":
                actions.edit.select_line()
            case "sentence":
                actions.edit.select_sentence()
            case "paragraph":
                actions.edit.select_paragraph()
            case "document":
                actions.edit.select_all()
            case _:
                return False
        return True

    if action_type in ["clearAndSetSelection", "remove"]:
        match scope_type:
            case "selection":
                actions.delete()
            case "token":
                actions.edit.delete_word()
            case "line":
                actions.edit.delete_line()
            case "sentence":
                actions.edit.delete_sentence()
            case "paragraph":
                actions.edit.delete_paragraph()
            case "document":
                actions.edit.delete_all()
            case _:
                return False
        return True

    if action_type == "setSelectionBefore":
        match scope_type:
            case "line":
                actions.edit.line_start()
            case "paragraph":
                actions.edit.paragraph_start()
            case "document":
                actions.edit.file_start()
            case _:
                return False
        return True

    if action_type == "setSelectionAfter":
        match scope_type:
            case "line":
                actions.edit.line_end()
            case "paragraph":
                actions.edit.paragraph_end()
            case "document":
                actions.edit.file_end()
            case _:
                return False
        return True

    if action_type == "editNewLineBefore":
        match scope_type:
            case "line":
                actions.edit.line_insert_up()
            case _:
                return False
        return True

    if action_type == "editNewLineAfter":
        match scope_type:
            case "line":
                actions.edit.line_insert_down()
            case _:
                return False
        return True

    if action_type == "insertCopyAfter":
        match scope_type:
            case "line":
                actions.edit.line_clone()
            case _:
                return False
        return True

    return False


simple_action_callbacks = {
    "setSelection": actions.skip,
    "setSelectionBefore": actions.edit.left,
    "setSelectionAfter": actions.edit.right,
    "copyToClipboard": actions.edit.copy,
    "cutToClipboard": actions.edit.cut,
    "pasteFromClipboard": actions.edit.paste,
    "clearAndSetSelection": actions.edit.delete,
    "remove": actions.edit.delete,
    "nextHomophone": actions.user.homophones_cycle_selected,
    "insertCopyAfter": actions.edit.selection_clone,
    # "editNewLineBefore":
    # "editNewLineAfter":
}

modifier_callbacks = {
    "extendThroughStartOf.line": actions.user.select_line_start,
    "extendThroughEndOf.line": actions.user.select_line_end,
    "containingScope.token": actions.edit.select_word,
    "containingScope.line": actions.edit.select_line,
    "containingScope.sentence": actions.edit.select_sentence,
    "containingScope.paragraph": actions.edit.select_paragraph,
    "containingScope.document": actions.edit.select_all,
}


def containing_token_if_empty():
    if actions.edit.selected_text() == "":
        actions.edit.select_word()


def get_action_callback(action: EditAction) -> Callable:
    action_type = action.type

    if action_type in simple_action_callbacks:
        return simple_action_callbacks[action_type]

    match action_type:
        case "insert":
            assert isinstance(action, EditInsertAction)
            return lambda: actions.insert(action.text)
        case "wrapWithPairedDelimiter":
            assert isinstance(action, EditWrapAction)
            return lambda: actions.user.delimiters_pair_wrap_selection(action.pair)
        case "applyFormatter":
            assert isinstance(action, EditFormatAction)
            return lambda: actions.user.reformat_selection(action.formatters)

    raise ValueError(f"Unknown Cursorless fallback action: {action}")


def get_modifier_callbacks(modifiers: list[dict]) -> list[Callable]:
    return [get_modifier_callback(modifier) for modifier in modifiers]


def get_modifier_callback(modifier: dict) -> Callable:
    modifier_type = modifier["type"]

    match modifier_type:
        case "containingTokenIfEmpty":
            return containing_token_if_empty
        case "containingScope":
            scope_type_type = modifier["scopeType"]
            return get_simple_modifier_callback(f"{modifier_type}.{scope_type_type}")
        case "extendThroughStartOf":
            if "modifiers" not in modifier:
                return get_simple_modifier_callback(f"{modifier_type}.line")
        case "extendThroughEndOf":
            if "modifiers" not in modifier:
                return get_simple_modifier_callback(f"{modifier_type}.line")

    raise ValueError(f"Unknown edit modifier: {modifier_type}")


def get_simple_modifier_callback(key: str) -> Callable:
    try:
        return modifier_callbacks[key]
    except KeyError:
        raise ValueError(f"Unknown edit modifier: {key}")
