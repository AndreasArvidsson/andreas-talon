from talon import Module, Context, actions
from .javascript import javascript_inserts

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.typescript
# Make typescript have precedence over c common
mode: command
"""

ctx.lists["self.code_data_type"] = {
    "bool": "boolean",
    "number": "number",
    "string": "string",
    "any": "any",
    "never": "never",
    "unknown": "unknown",
    "object": "object",
    "void": "void",
    "null": "null",
    "undefined": "undefined",
}

ctx.lists["self.code_insert"] = {
    **javascript_inserts,
    **{
        "public": "public ",
        "private": "private ",
        "protected": "protected ",
        "readonly": "readonly ",
        "interface": "interface ",
        "type": "type ",
    },
}


@ctx.action_class("user")
class UserActions:
    # Insert types
    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" => {type}")
