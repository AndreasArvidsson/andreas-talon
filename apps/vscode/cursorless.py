from talon import Module, Context, actions
from typing import Any
import os

mod = Module()

ctx = Context()
ctx.matches = r"""
mode: command
"""

fallback_action_callbacks = {
    "setSelection": actions.skip,
    "copyToClipboard": actions.edit.copy,
    "cutToClipboard": actions.edit.cut,
    "pasteFromClipboard": actions.edit.paste,
    "clearAndSetSelection": actions.edit.delete,
    "remove": actions.edit.delete,
    "applyFormatter": actions.user.reformat_selection,
    "editNewLineBefore": actions.edit.line_insert_up,
    "editNewLineAfter": actions.edit.line_insert_down,
    "nextHomophone": actions.user.homophones_cycle_selected,
    "wrapWithPairedDelimiter.pairedDelimiter": lambda pair: actions.user.delimiters_pair_wrap_selection_with(
        pair[0], pair[1]
    ),
}

fallback_target_callbacks = {
    "selection": actions.skip,
    "extendThroughStartOf": actions.user.select_line_start,
    "extendThroughEndOf": actions.user.select_line_end,
    "containing_document": actions.edit.select_all,
    "containing_paragraph": actions.edit.select_paragraph,
    "containing_line": actions.edit.select_line,
    "containing_token": actions.edit.select_word,
}


@ctx.action_class("user")
class UserActions:
    def cursorless_command(action_id: str, target: dict):
        if use_fallback(target):
            perform_fallback_command(action_id, target)
        else:
            actions.next(action_id, target)

    def cursorless_reformat(target: dict, formatters: str):
        if use_fallback(target):
            perform_fallback_command("applyFormatter", target, formatters)
        else:
            actions.next(target, formatters)

    def cursorless_wrap(action_type: str, target: dict, cursorless_wrapper):
        if use_fallback(target):
            perform_fallback_command(
                f"{action_type}.{cursorless_wrapper.type}",
                target,
                cursorless_wrapper.extra_args,
            )
        else:
            actions.next(action_type, target, cursorless_wrapper)


def perform_fallback_command(action_id: str, target: dict, args: Any = None):
    """Perform non Cursorless fallback command"""
    actions.user.debug(
        "Current command targets selection and is not in a text editor. Perform fallback command."
    )
    try:
        action_callback = get_fallback_action_callback(action_id)
        target_callback = get_fallback_target_callback(target)
        target_callback()
        if args is not None:
            action_callback(args)
        else:
            action_callback()
    except Exception as ex:
        actions.app.notify(str(ex))


def get_fallback_action_callback(action_id: str):
    if action_id in fallback_action_callbacks:
        return fallback_action_callbacks[action_id]
    raise Exception(f"Unknown Cursorless fallback action: {action_id}")


def get_fallback_target_callback(target: dict):
    if "modifiers" not in target:
        return fallback_target_callbacks["selection"]
    if len(target["modifiers"]) == 1:
        modifier = target["modifiers"][0]
        modifier_type = modifier["type"]
        if modifier_type == "containingScope":
            modifier_type = f"containing_{modifier['scopeType']['type']}"
        if modifier_type in fallback_target_callbacks:
            return fallback_target_callbacks[modifier_type]
        raise Exception(f"Unknown Cursorless fallback modifier type: {modifier_type}")
    raise Exception(f"Unknown Cursorless fallback target: {target}")


def use_fallback(target: dict) -> bool:
    return target_is_selection(target) and not focused_element_is_text_editor()


def target_is_selection(target: dict) -> bool:
    if target["type"] != "primitive":
        return False
    mark = target.get("mark")
    return not mark or mark["type"] == "cursor"


def focused_element_is_text_editor() -> bool:
    element_type = actions.user.vscode_get("command-server.getFocusedElementType")
    return element_type == "textEditor"


@mod.action_class
class Actions:
    def cursorless_use_release():
        """Use main branch of cursorless-talon"""
        switch_folder(True)

    def cursorless_use_develop():
        """Use developed folder of cursorless-talon"""
        switch_folder(False)

    def cursorless_browser_open_target(target: Any):
        """Search for target text in browser"""
        texts = actions.user.cursorless_single_target_command_get(
            "getText",
            target,
        )
        text = " + ".join(texts)
        actions.user.browser_open(text)

    def cursorless_wrap_target_with_symbol(target: Any, symbol: str):
        """Wrap the target with <symbol>"""
        if symbol == "space":
            symbol = " "
        delimiters = [symbol, symbol]
        actions.user.cursorless_single_target_command_with_arg_list(
            "wrapWithPairedDelimiter", target, delimiters
        )


def switch_folder(useRelease: bool):
    if useRelease:
        targetPath = "cursorless-talon"
    else:
        targetPath = "cursorless\\cursorless-talon"
    target = f"{actions.path.user_home()}\\repositories\\{targetPath}"
    link = f"{actions.path.talon_user()}\\cursorless-talon"
    actions.user.debug(f"cmd /c mklink /d {link} {target}")
    os.system(f"cmd /c rmdir {link}")
    os.system(f"cmd /c mklink /J {link} {target}")
    actions.sleep("500ms")
    actions.user.talon_restart()
