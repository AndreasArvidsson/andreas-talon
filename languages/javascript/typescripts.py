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

# fmt: off
types = {
    "any"       : "any",
    "bool"      : "boolean",
    "never"     : "never",
    "null"      : "null",
    "number"    : "number",
    "object"    : "object",
    "regex"     : "RegExp",
    "string"    : "string",
    "undefined" : "undefined",
    "unknown"   : "unknown",
    "void"      : "void",
    "funk"      : "() => void",
    "record"    : "Record"
}

ctx.lists["user.code_data_type"] = {
    **types,
    **{f"{k} list": f"{v}[]" for k, v in types.items()},
}
ctx.lists["user.code_function_modifier"] = {
    "public",
    "private",
    "protected",
}
ctx.lists["user.code_insert"] = {
    **javascript_inserts,
    **{
        "public"    : "public ",
        "private"   : "private ",
        "protected" : "protected ",
        "readonly"  : "readonly ",
        "interface" : "interface ",
        "type"      : " type ",
        "key of"    : "keyof ",
        "as"        : " as ",
    },
}
# fmt: on


@ctx.action_class("user")
class UserActions:
    # Insert types
    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" => {type}")
