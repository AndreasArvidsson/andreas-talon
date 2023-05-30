from talon import Context, actions

ctx = Context()

ctx.matches = r"""
tag: user.markdown
"""

ctx.tags = ["user.generic_language"]


@ctx.action_class("user")
class UserActions:
    def code_link(text: str = ""):
        actions.user.insert_snippet(f"[{text}$0]({actions.clip.text()})")
