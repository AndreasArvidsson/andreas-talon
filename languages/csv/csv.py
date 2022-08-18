from talon import Context, actions

ctx = Context()

ctx.matches = r"""
tag: user.csv
"""

ctx.tags = ["user.comments"]


@ctx.action_class("user")
class UserActions:
    def comments_insert(text: str = ""):
        actions.insert(f"# {text}")
