from talon import Module, actions
from typing import Any
import os
from ...core.snippets.snippet_types import InsertionSnippet, WrapperSnippet


mod = Module()


@mod.action_class
class Actions:
    def c_use_release():
        """Use main branch of cursorless-talon"""
        switch_folder(True)

    def c_use_develop():
        """Use developed folder of cursorless-talon"""
        switch_folder(False)

    def c_browser_open_target(target: Any):
        """Search for target text in browser"""
        texts = actions.user.cursorless_get_text_list(target)
        text = " + ".join(texts)
        actions.user.browser_open(text)

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

    def c_insert_snippet(destination: Any, name: str):
        """Insert cursorless snippet <name>"""
        snippet: InsertionSnippet = actions.user.get_insertion_snippet(name)

        actions.user.cursorless_insert_snippet(
            snippet.body, destination, snippet.scopes
        )

    def c_wrap_with_snippet(target: Any, name: str):
        """Wrap the target with snippet <name>"""
        snippet: WrapperSnippet = actions.user.get_wrapper_snippet(name)

        actions.user.cursorless_wrap_with_snippet(
            snippet.body, target, snippet.variable_name, snippet.scope
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
