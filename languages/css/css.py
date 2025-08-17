from talon import Context, actions

ctx = Context()
ctx.matches = r"""
code.language: css
code.language: scss
"""


@ctx.action_class("user")
class UserActions:
    # Variable statement
    def code_variable(assign: bool, modifiers: list[str], data_type: str, name: str):
        snippet = name or "$1"
        if modifiers:
            raise ValueError(f"Modifiers not supported in CSS: {modifiers}")
        if data_type:
            raise ValueError(f"Data type not supported in CSS: {data_type}")
        if assign:
            snippet += ": $0"
        actions.user.insert_snippet(snippet)
