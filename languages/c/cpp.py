from talon import Module, Context, actions
from .c import c_code_insert

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: cpp
# Make typescript win over C
mode: command
"""


ctx.lists["user.code_insert"] = {
    **c_code_insert,
    "this": "this",
    "include": "#include ",
    "new": "new ",
    "class": "class ",
    "throw": "throw ",
}


@ctx.action_class("user")
class UserActions:
    # Class declaration
    def code_class(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name(
            "classDeclaration",
            {"name": name},
        )

    # Constructor declaration
    def code_constructor(modifiers: list[str]):
        name = actions.user.code_get_class_name()
        if not name:
            raise ValueError("Class name not found")
        actions.user.insert_snippet_by_name(
            "constructorDeclaration",
            {"name": name},
        )
