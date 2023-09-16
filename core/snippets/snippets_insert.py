from talon import Module, actions
import re
from .snippet_types import Snippet

mod = Module()


@mod.action_class
class Actions:
    # Default implementation inserts snippets as normal text
    def insert_snippet(snippet: str):
        """Insert snippet"""
        lines = snippet.splitlines()
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
            # Update existing line
            lines[i] = line

        updated_snippet = "\n".join(lines)
        actions.insert(updated_snippet)

        if found_stop:
            up(len(lines) - stop_row - 1)
            actions.edit.line_start()
            right(stop_col)

    def insert_snippet_by_name(name: str, substitutions: dict[str, str] = None):
        """Insert snippet <name>"""
        snippet: Snippet = actions.user.get_snippet(name)
        body = snippet.body
        if substitutions:
            for k, v in substitutions.items():
                body = body.replace(f"${k}", v)
        actions.user.insert_snippet(body)

    def code_insert_snippet_by_name(name: str, substitutions: dict[str, str] = None):
        """Insert snippet <name> for the current programming language"""
        lang = actions.code.language()
        actions.user.insert_snippet_by_name(f"{lang}.{name}", substitutions)


def up(n: int):
    """Move cursor up <n> rows"""
    for _ in range(n):
        actions.edit.up()


def right(n: int):
    """Move cursor right <n> columns"""
    for _ in range(n):
        actions.edit.right()
