from talon import Context, Module, actions
from urllib.parse import urlparse

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: markdown
"""

mod.list("markdown_pair", "List of markdown format delimiters")
ctx.lists["self.markdown_pair"] = {
    "bold": "**",
    "italic": "_",
}


@mod.action_class
class UserActions:
    def code_markdown_link(text: str = ""):
        """Insert link <text>"""
        link = actions.clip.text()
        if is_valid_link(link):
            actions.user.insert_snippet_by_name(
                "linkWithUri", {"text": text, "uri": link}
            )
        else:
            actions.user.insert_snippet_by_name("link", {"text": text})


def is_valid_link(link: str) -> bool:
    # Multiline strings can't be a link
    return link and "\n" not in link and "." in urlparse(link).netloc
