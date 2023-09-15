from talon import Module, actions

mod = Module()
mod.tag("code_comments")


@mod.action_class
class Actions:
    def code_comment_insert(text: str):
        """Insert inline comment"""
        insert_comment("commentLine", text)

    def code_comment_insert_block(text: str):
        """Insert block comment"""
        insert_comment("commentBlock", text)

    def code_comment_insert_docstring(text: str):
        """Insert documentation string/comment"""
        insert_comment("commentDocumentation", text)


def insert_comment(name: str, text: str):
    text = actions.user.format_text(text, "SENTENCE")
    actions.user.code_insert_snippet_by_name(
        name,
        {"0": f"{text}$0"},
    )
