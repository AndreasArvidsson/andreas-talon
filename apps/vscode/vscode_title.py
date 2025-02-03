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


@ctx.action_class("win")
class WinActions:
    def filename():
        title: str = actions.win.title()
        index = title.find(" (Working Tree)")
        if index != -1:
            filename = title[:index]
        else:
            filename = actions.win.title().split(" - ")[0]
        if is_untitled(filename):
            return get_untitled_name(filename)
        if "." in filename:
            return filename
        return ""


@ctx_lang.action_class("code")
class LangCodeActions:
    def language() -> Union[str, set[str]]:
        # New untitled files are markdown in vscode
        if is_untitled(actions.win.filename()):
            return "markdown"
        return actions.next()


UNTITLED_RE = re.compile(r"Untitled-\d$")


def is_untitled(filename: str):
    return UNTITLED_RE.search(filename) is not None


def get_untitled_name(filename: str):
    return UNTITLED_RE.search(filename).group()
