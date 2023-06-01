from talon import Module, Context, actions
import os

mod = Module()
ctx = Context()

fallback_action_callbacks = {
    "setSelection": actions.skip,
    "copyToClipboard": actions.edit.copy,
    "cutToClipboard": actions.edit.cut,
    "pasteFromClipboard": actions.edit.paste,
    "clearAndSetSelection": actions.edit.delete,
    "remove": actions.edit.delete,
}
# paste to line

fallback_target_callbacks = {
    "extendThroughStartOf": actions.user.select_line_start,
    "extendThroughEndOf": actions.user.select_line_end,
    "containing_document": actions.edit.select_all,
    "containing_paragraph": actions.edit.select_paragraph,
    "containing_line": actions.edit.select_line,
    "containing_word": actions.edit.select_word,
}


@ctx.action_class("user")
class UserActions:
    def cursorless_command(action_id: str, target: dict):
        if target_is_selection(target) and not focused_element_is_text_editor():
            perform_fallback_command(action_id, target)
        else:
            actions.next(action_id, target)


def perform_fallback_command(action_id: str, target: dict):
    """Perform non Cursorless fallback command"""
    actions.user.debug(
        "Current command targets selection and is not in a text editor. Perform fallback command."
    )
    try:
        action_callback = get_fallback_action_callback(action_id)
        target_callback = get_fallback_target_callback(target)
        target_callback()
        action_callback()
    except Exception as ex:
        actions.app.notify(str(ex))


def get_fallback_action_callback(action_id: str):
    if action_id in fallback_action_callbacks:
        return fallback_action_callbacks[action_id]
    raise Exception(f"Unknown Cursorless fallback action: {action_id}")


def get_fallback_target_callback(target: dict):
    if len(target["modifiers"]) == 1:
        modifier = target["modifiers"][0]
        modifier_type = modifier["type"]
        if modifier_type == "containingScope":
            modifier_type = f"containing_{modifier['scopeType']['type']}"
        if modifier_type in fallback_target_callbacks:
            return fallback_target_callbacks[modifier_type]
        raise Exception(f"Unknown Cursorless fallback target type: {modifier_type}")
    raise Exception(f"Unknown Cursorless fallback target: {target}")


def focused_element_is_text_editor() -> bool:
    element_type = actions.user.vscode_get("command-server.getFocusedElementType")
    return element_type == "textEditor"


def target_is_selection(target: dict) -> bool:
    if target["type"] != "primitive":
        return False
    mark = target.get("mark")
    return not mark or mark["type"] == "cursor"


@mod.action_class
class Actions:
    def cursorless_use_release():
        """Use main branch of cursorless-talon"""
        switch_folder(f"{actions.path.user_home()}\\cursorless-talon")

    def cursorless_use_develop():
        """Use developed folder of cursorless-talon"""
        switch_folder(f"{actions.path.user_home()}\\cursorless\\cursorless-talon")

    def cursorless_browser_open_target(target: dict):
        """Search for target text in browser"""
        texts = actions.user.cursorless_single_target_command_get(
            "getText",
            target,
        )
        text = " + ".join(texts)
        actions.user.browser_open(text)

    def cursorless_wrap_target_with_symbol(target: dict, symbol: str):
        """Wrap the target with the given symbol"""
        if symbol == "space":
            symbol = " "
        delimiters = [symbol, symbol]
        actions.user.cursorless_single_target_command_with_arg_list(
            "wrapWithPairedDelimiter", target, delimiters
        )


def switch_folder(target: str):
    link = f"{actions.path.talon_user()}\\cursorless-talon"
    actions.user.debug(f"cmd /c mklink /d {link} {target}")
    os.system(f"cmd /c rmdir {link}")
    os.system(f"cmd /c mklink /d {link} {target}")
    actions.sleep("500ms")
    actions.user.talon_restart()
