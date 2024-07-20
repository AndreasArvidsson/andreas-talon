from talon import Module, actions
from .edit_command_actions import EditAction, get_action_callback
from .edit_command_modifiers import EditModifier, get_modifier_callbacks

# fmt: off
compound_actions = {
    "setSelection.containingScope(token)":              actions.edit.select_word,
    "setSelection.containingScope(line)":               actions.edit.select_line,
    "setSelection.containingScope(sentence)":           actions.edit.select_sentence,
    "setSelection.containingScope(paragraph)":          actions.edit.select_paragraph,
    "setSelection.containingScope(document)":           actions.edit.select_all,

    "setSelectionBefore.containingScope(line)":         actions.edit.line_start,
    "setSelectionBefore.containingScope(paragraph)":    actions.edit.paragraph_start,
    "setSelectionBefore.containingScope(document)":     actions.edit.file_start,

    "setSelectionAfter.containingScope(line)":          actions.edit.line_end,
    "setSelectionAfter.containingScope(paragraph)":     actions.edit.paragraph_end,
    "setSelectionAfter.containingScope(document)":      actions.edit.file_end,

    "remove.containingScope(token)":                    actions.edit.delete_word,
    "remove.containingScope(line)":                     actions.edit.delete_line,
    "remove.containingScope(sentence)":                 actions.edit.delete_sentence,
    "remove.containingScope(paragraph)":                actions.edit.delete_paragraph,
    "remove.containingScope(document)":                 actions.edit.delete_all,

    "editNewLineBefore.containingTokenIfEmpty":         actions.edit.line_insert_up,
    "editNewLineBefore.containingScope(line)":          actions.edit.line_insert_up,
    "editNewLineBefore.containingScope(paragraph)":     actions.user.paragraph_insert_up,

    "editNewLineAfter.containingTokenIfEmpty":          actions.edit.line_insert_down,
    "editNewLineAfter.containingScope(line)":           actions.edit.line_insert_down,
    "editNewLineAfter.containingScope(paragraph)":      actions.user.paragraph_insert_down,

    "insertCopyBefore.containingTokenIfEmpty":          actions.user.line_clone_up,
    "insertCopyBefore.containingScope(line)":           actions.user.line_clone_up,
    "insertCopyBefore.containingScope(paragraph)":      actions.user.paragraph_clone_up,

    "insertCopyAfter.containingTokenIfEmpty":           actions.edit.line_clone,
    "insertCopyAfter.containingScope(line)":            actions.edit.line_clone,
    "insertCopyAfter.containingScope(paragraph)":       actions.user.paragraph_clone_down,
}
# fmt: on


mod = Module()


@mod.capture(rule="<user.edit_modifier>+")
def edit_target(m) -> list[EditModifier]:
    return m.edit_modifier_list


@mod.action_class
class Actions:
    def edit_command(action: EditAction, modifiers: list[EditModifier]):
        """Perform edit command"""

        # string joined of action and modifiers
        key = str(action) + "." + ".".join([str(modifier) for modifier in modifiers])

        if key in compound_actions:
            compound_actions[key]()
            return

        action_callback = get_action_callback(action)
        modifier_callbacks = get_modifier_callbacks(modifiers)

        for callback in reversed(modifier_callbacks):
            callback()

        action_callback()

    def edit_command_bring(source: list[EditModifier], destination: list[EditModifier]):
        """Perform edit bring command"""
        source_modifier_callbacks = get_modifier_callbacks(source)
        destination_modifier_callbacks = get_modifier_callbacks(destination)

        for callback in reversed(source_modifier_callbacks):
            callback()

        source_text = actions.edit.selected_text()

        for callback in reversed(destination_modifier_callbacks):
            callback()

        actions.insert(source_text)
