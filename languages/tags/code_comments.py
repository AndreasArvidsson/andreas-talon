from typing import Optional
from talon import Module, actions

mod = Module()
mod.tag("code_comments")


@mod.action_class
class Actions:
    def insert_todo_comment_snippet(message: Optional[str] = None):
        """Inserts a TODO comment snippet"""
        message = actions.user.format_text(message or "", "SENTENCE")
        actions.user.insert_snippet_by_name("commentLine", {"msg": f"TODO: {message}"})

    def insert_fixme_comment_snippet(message: Optional[str] = None):
        """Inserts a FIXME comment snippet"""
        message = actions.user.format_text(message or "", "SENTENCE")
        actions.user.insert_snippet_by_name("commentLine", {"msg": f"FIXME: {message}"})
