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

LANGUAGE_RE = re.compile(r"\[(\w+)\]$")


@ctx.action_class("win")
class WinActions:
    def filename() -> str:
        title: str = actions.win.title()
        # Git diff view, unstated changes: "MyFile.txt (Working Tree)"
        index = title.find(" (Working Tree)")
        if index > -1:
            return title[:index]
        # Git diff view, staged changes: "MyFile.txt (Index)"
        index = title.find(" (Index)")
        if index > -1:
            return title[:index]
        # Normal file: "MyFile.txt | MyWorkspace"
        return title.split(" | ", 1)[0]


@ctx_lang.action_class("code")
class LangCodeActions:
    def language() -> Union[str, set[str]]:
        title: str = actions.win.title()
        match = LANGUAGE_RE.search(title)
        if match is not None:
            return match.group(1)
        return ""
