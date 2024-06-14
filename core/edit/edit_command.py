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

    "editNewLineBefore.containingScope(line)":          actions.edit.line_insert_up,
    "editNewLineBefore.containingTokenIfEmpty":         actions.edit.line_insert_up,

    "editNewLineAfter.containingScope(line)":           actions.edit.line_insert_down,
    "editNewLineAfter.containingTokenIfEmpty":          actions.edit.line_insert_down,

    "insertCopyAfter.containingScope(line)":            actions.edit.line_clone,
    "insertCopyAfter.containingTokenIfEmpty":           actions.edit.line_clone,
}
# fmt: on


mod = Module()


@mod.action_class
class Actions:
    def edit_command(action: EditAction, modifiers: list[EditModifier]):
        """Perform edit command"""

        # string joined of action and modifiers
        key = str(action) + "." + ".".join([str(modifier) for modifier in modifiers])

        print(key)

        if key in compound_actions:
            compound_actions[key]()
            return

        try:
            action_callback = get_action_callback(action)
            modifier_callbacks = get_modifier_callbacks(modifiers)
            for callback in reversed(modifier_callbacks):
                callback()
            return action_callback()
        except ValueError as ex:
            actions.user.notify(str(ex))
