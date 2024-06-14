from dataclasses import dataclass
from typing import Callable, Literal, Union
from talon import Module, actions

EditSimpleActionType = Literal[
    "setSelection",
    "setSelectionBefore",
    "setSelectionAfter",
    "clearAndSetSelection",
    "remove",
    "copyToClipboard",
    "cutToClipboard",
    "pasteFromClipboard",
    "editNewLineBefore",
    "editNewLineAfter",
    "insertCopyBefore",
    "insertCopyAfter",
    "nextHomophone",
    "searchEngine",
]


@dataclass
class EditSimpleAction:
    type: EditSimpleActionType

    def __str__(self):
        return self.type


@dataclass
class EditInsertAction:
    type = "insert"
    text: str

    def __str__(self):
        return self.type


@dataclass
class EditWrapAction:
    type = "wrapWithPairedDelimiter"
    pair: str

    def __str__(self):
        return self.type


@dataclass
class EditFormatAction:
    type = "applyFormatter"
    formatters: str

    def __str__(self):
        return self.type


EditAction = Union[
    EditSimpleAction,
    EditInsertAction,
    EditWrapAction,
    EditFormatAction,
]


mod = Module()
mod.list("edit_simple_action", desc="Actions for the edit command")


@mod.capture(rule="{user.edit_simple_action}")
def edit_simple_action(m) -> EditSimpleAction:
    if m.edit_simple_action == "clearAndSetSelection":
        return EditSimpleAction("remove")
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


simple_action_callbacks: dict[EditSimpleActionType, Callable] = {
    "setSelection": actions.skip,
    "setSelectionBefore": actions.edit.left,
    "setSelectionAfter": actions.edit.right,
    "copyToClipboard": actions.edit.copy,
    "cutToClipboard": actions.edit.cut,
    "pasteFromClipboard": actions.edit.paste,
    "clearAndSetSelection": actions.edit.delete,
    "remove": actions.edit.delete,
    "nextHomophone": actions.user.homophones_cycle_selected,
    "insertCopyBefore": actions.user.selection_clone_before,
    "insertCopyAfter": actions.edit.selection_clone,
    "editNewLineBefore": lambda: actions.key("left space left"),
    "editNewLineAfter": lambda: actions.key("right space"),
    "searchEngine": actions.user.browser_search_selected,
}


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

    raise ValueError(f"Unknown edit action: {action}")
