from talon import Module, Context, actions
from typing import Union
import re
from .snippet_types import Snippet

mod = Module()

ctx_vscode = Context()
ctx_vscode.matches = r"""
app: vscode
"""


@mod.action_class
class Actions:
    # Default implementation inserts snippets as normal text
    def insert_snippet(snippet: Union[str, list[str]]):
        """Insert snippet"""
        lines = split_snippet(snippet)
        found_stop = False
        for i, line in enumerate(lines):
            # Some IM services will send the message on a tab
            line = re.sub(r"\t+", "    ", line)

            if found_stop != "$1":
                if "$1" in line:
                    found_stop = "$1"
                    stop_row = i
                    stop_col = line.index("$1")
                elif "$0" in line:
                    found_stop = "$0"
                    stop_row = i
                    stop_col = line.index("$0")

            # Replace placeholders with default text
            line = re.sub(r"\$\{\d+:(.*?)\}", r"\1", line)
            # Remove tab stops
            line = re.sub(r"\$\d+", "", line)

            if i > 0:
                actions.edit.line_insert_down()
            actions.insert(line)

        if found_stop:
            up(len(lines) - stop_row - 1)
            actions.edit.line_start()
            right(stop_col)

    def insert_snippet_by_name(name: str, substitutions: dict[str, str] = None):
        """Insert snippet with name <name>"""
        snippet: Snippet = actions.user.get_snippet(name)
        body = snippet.body
        if substitutions:
            for k, v in substitutions.items():
                body = body.replace(f"${k}", v)
        actions.user.insert_snippet(body)


@ctx_vscode.action_class("user")
class VscodeActions:
    # Vscode has proper support for snippets
    def insert_snippet(snippet: Union[str, list[str]]):
        if isinstance(snippet, list):
            snippet = "\n".join(snippet)

        actions.user.vscode("editor.action.insertSnippet", {"snippet": snippet})
        # actions.user.cursorless_insert_snippet(snippet)


def split_snippet(snippet: Union[str, list[str]]) -> list[str]:
    if isinstance(snippet, list):
        return snippet
    lines = snippet.split("\n")
    # Clean leading whitespaces(not tabs) in case this was a multiline string
    return [line.lstrip(" ") for line in lines]


def up(n: int):
    """Move cursor up <n> rows"""
    for _ in range(n):
        actions.edit.up()


def right(n: int):
    """Move cursor right <n> columns"""
    for _ in range(n):
        actions.edit.right()
