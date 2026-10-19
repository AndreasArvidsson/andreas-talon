import os
from typing import Any

from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def c_use_release():
        """Use main branch of cursorless-talon"""
        switch_folder(True)

    def c_use_develop():
        """Use developed folder of cursorless-talon"""
        switch_folder(False)

    @staticmethod
    def c_browser_search_target(target: Any):
        """Search for target text in browser"""
        texts = actions.user.cursorless_get_text_list(target)
        text = " + ".join(texts)
        actions.user.browser_search(text)

    @staticmethod
    def c_search_file(target: Any):
        """Search for file with name of target text"""
        text = actions.user.cursorless_get_text(target)
        actions.user.find_file(text)

    @staticmethod
    def c_wrap_with_symbol(target: Any, symbol: str):
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


def switch_folder(useRelease: bool):
    link = rf"{actions.path.talon_user()}\\cursorless-talon"

    if useRelease:
        target = r"D:\talon-user\cursorless-talon"
    else:
        target = r"D:\repositories\cursorless\cursorless-talon"

    os.system(f"cmd /c rmdir {link}")
    os.system(f"cmd /c mklink /J {link} {target}")

    actions.sleep("500ms")
    actions.user.talon_restart()
