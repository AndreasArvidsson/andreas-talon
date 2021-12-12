from talon import Module, Context, actions
from typing import Union
import re

mod = Module()

ctx_vscode = Context()
ctx_vscode.matches = r"""
app: vscode
"""


@mod.action_class
class Actions:
    # Default implementation inserts snippets as normal text
    def insert_snippet(snippet: Union[str, list[str]]):
        """Inserts a snippet"""
        lines = split_snippet(snippet)
        for i in range(len(lines)):
            if i > 0:
                actions.edit.line_insert_down()
            line = lines[i]
            # Replace placeholders with default text
            line = re.sub(r"\$\{\d+:(.*?)\}", r"\1", line)
            # Remove tab stops
            line = re.sub(r"\$\d+", "", line)
            # Some IM services will send the message on a tab
            line = re.sub(r"[\t]+", "    ", line)
            actions.insert(line)


@ctx_vscode.action_class("user")
class VscodeActions:
    # Vscode has proper support for snippets
    def insert_snippet(snippet: Union[str, list[str]]):
        lines = split_snippet(snippet)
        snippet = "\n".join(lines)
        actions.user.vscode("editor.action.insertSnippet", {"snippet": snippet})


def split_snippet(snippet: Union[str, list[str]]) -> list[str]:
    if isinstance(snippet, list):
        return snippet
    lines = snippet.split("\n")
    # Clean leading whitespaces in case this was a multiline string
    for i in range(len(lines)):
        lines[i] = lines[i].lstrip(" ")
    return lines
