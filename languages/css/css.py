from talon import Context, actions


ctx = Context()
ctx.matches = r"""
tag: user.css
"""


@ctx.action_class("user")
class UserActions:
    # Variable statement
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if assign:
            text += ": "
        actions.insert(text)

    # Formatting getters
    def code_get_variable_format() -> str:
        return "DASH_SEPARATED"
