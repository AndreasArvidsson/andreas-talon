from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.markdown
"""

ctx.tags = ["user.generic_language"]

@ctx.action_class("user")
class UserActions:
    def code_link():
        actions.user.insert_snippet(f"[$0]({actions.clip.text()})")
