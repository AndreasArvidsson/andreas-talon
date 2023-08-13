from talon import Module, Context, actions
from .javascript import javascript_inserts

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: typescript
code.language: typescriptreact
# Make typescript win over javascript
mode: command
"""

types = {
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

ctx.lists["self.code_data_type"] = {
    **types,
    **{f"{k} list": f"{v}[]" for k, v in types.items()},
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
        "key of": "keyof ",
        "as": " as ",
    },
}


@ctx.action_class("user")
class UserActions:
    # Insert types
    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" => {type}")
