from typing import Union
from talon import Context, actions
import re


ctx = Context()
ctx.matches = r"""
app: vscode
"""

ctx_lang = Context()
ctx_lang.matches = r"""
app: vscode
not tag: user.code_language_forced
"""

ctx_not_editor = Context()
ctx_not_editor.matches = r"""
app: vscode
not win.title: /\[Text Editor\]/
"""

FILENAME_DELIMITERS = [
    # Normal file: "MyFile.txt | ..."
    " | ",
    # Git diff view, unstaged changes: "MyFile.txt (Working Tree) ..."
    " (Working Tree) ",
    # Git diff view, staged changes: "MyFile.txt (Index) ..."
    " (Index) ",
]
FILENAME_RE = re.compile("|".join(re.escape(d) for d in FILENAME_DELIMITERS))
LANGUAGE_RE = re.compile(r"\[(\w+)\]$")


@ctx.action_class("win")
class WinActions:
    def filename() -> str:
        title: str = actions.win.title()
        match = FILENAME_RE.search(title)
        if match is not None:
            return title[: match.start()]
        return ""


@ctx_lang.action_class("code")
class LangCodeActions:
    def language() -> Union[str, set[str]]:
        title: str = actions.win.title()
        match = LANGUAGE_RE.search(title)
        if match is not None:
            return match.group(1)
        return ""


@ctx_not_editor.action_class("edit")
class NotEditorEditActions:
    def line_insert_up():
        actions.key("home")
        actions.sleep("10ms")
        actions.key("shift-enter up")

    def line_insert_down():
        actions.key("end")
        actions.sleep("10ms")
        actions.key("shift-enter")
