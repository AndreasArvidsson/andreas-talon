from talon import Module, actions
from typing import Any
import os

mod = Module()


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
        texts = actions.user.private_cursorless_command_get(
            {
                "name": "getText",
                "target": target,
            }
        )

        text = " + ".join(texts)
        actions.user.browser_open(text)

    def cursorless_wrap_with_symbol(target: Any, symbol: str):
        """Wrap the target with <symbol>"""
        if symbol == "space":
            symbol = " "

        actions.user.private_cursorless_command_and_wait(
            {
                "name": "wrapWithPairedDelimiter",
                "left": symbol,
                "right": symbol,
                "target": target,
            }
        )

    def cursorless_my_wrap_with_snippet(target: Any, id: str):
        """Wrap the target with snippet <id>"""
        snippet = actions.user.get_snippet(id)
        variable_name = id.split(".")[-1]
        body = snippet.body.replace(f"${variable_name}", f"$TM_SELECTED_TEXT")
        actions.user.cursorless_wrap_with_snippet(
            body, target, None, snippet.wrapperScope
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
