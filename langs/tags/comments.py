from talon import Module

mod = Module()
mod.tag("comments")


@mod.action_class
class Actions:
    def comments_insert(text: str = ""):
        """Insert inline comment"""

    def comments_insert_block(text: str = ""):
        """Insert block comment"""
