from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.markdown
"""

mod.list("markdown_pair", desc="List of markdown format delimiters")
ctx.lists["self.markdown_pair"] = {
    "bold": "**",
    "italic": "_",
}


@ctx.action_class("user")
class UserActions:
    def code_link(text: str = ""):
        link = actions.clip.text()
        if is_valid_link(link):
            actions.user.code_insert_snippet("linkWithUri", {"text": text, "uri": link})
        else:
            actions.user.code_insert_snippet("link", {"text": text})


def is_valid_link(link: str) -> bool:
    # Multiline strings can't be a link
    return link and "\n" not in link
