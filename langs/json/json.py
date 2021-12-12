from talon import Module, Context, actions

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.json
"""


@ctx.action_class("user")
class UserActions:
    # Comments
    def comments_insert(text: str = ""):
        actions.insert(f"// {text}")

    def comments_insert_block(text: str = ""):
        actions.user.comments_insert(text)
