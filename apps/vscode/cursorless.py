from talon import Module, actions
from typing import Any
import os

mod = Module()


@mod.action_class
class Actions:
    def c_use_release():
        """Use main branch of cursorless-talon"""
        switch_folder(True)

    def c_use_develop():
        """Use developed folder of cursorless-talon"""
        switch_folder(False)

    def c_browser_search_target(target: Any):
        """Search for target text in browser"""
        texts = actions.user.cursorless_get_text_list(target)
        text = " + ".join(texts)
        actions.user.browser_search(text)

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
    link = f"{actions.path.talon_user()}\\cursorless-talon"
    link_dev = f"{actions.path.talon_user()}\\cursorless-talon-dev"
    repos = f"{actions.path.user_home()}\\repositories"
    target_path = "cursorless-talon" if useRelease else "cursorless\\cursorless-talon"
    target = f"{repos}\\{target_path}"
    target_dev = f"{repos}\\cursorless\\cursorless-talon-dev"

    os.system(f"cmd /c rmdir {link}")
    os.system(f"cmd /c mklink /J {link} {target}")

    os.system(f"cmd /c rmdir {link_dev}")
    os.system(f"cmd /c mklink /J {link_dev} {target_dev}")

    actions.sleep("500ms")
    actions.user.talon_restart()
