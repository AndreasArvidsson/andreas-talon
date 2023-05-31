from talon import Module, Context, actions
import os

mod = Module()
ctx = Context()


@ctx.action_class("user")
class UserActions:
    def cursorless_command(action_id: str, target: dict):
        if target_is_selection(target) and not focused_element_is_text_editor():
            perform_fallback_command(action_id, target)
        else:
            actions.next(action_id, target)


def perform_fallback_command(action_id: str, target: dict):
    """Perform non Cursorless fallback command"""
    print(
        "Current command targets selection and is not in a text editor. Perform fallback command"
    )
    print(action_id)
    print(target)


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
