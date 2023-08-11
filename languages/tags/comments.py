from talon import Module, actions, settings

mod = Module()
mod.tag("comments")


@mod.action_class
class Actions:
    def comment_insert(text: str):
        """Insert inline comment"""
        insert_comment("commentLine", text)

    def comment_insert_block(text: str):
        """Insert block comment"""
        insert_comment("commentBlock", text)

    def comment_insert_docstring(text: str):
        """Insert documentation string/comment"""
        insert_comment("commentDocumentation", text)


def insert_comment(name: str, text: str):
    text = actions.user.format_text(text, "SENTENCE")
    lang = settings.get("user.code_lang")
    actions.user.insert_snippet_by_name(
        f"{lang}.{name}",
        {"0": f"{text}$0"},
    )
