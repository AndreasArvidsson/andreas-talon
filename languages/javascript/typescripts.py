from talon import Module, Context, actions
from .javascript import js_keywords

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: typescript
code.language: typescriptreact
# Make typescript win over javascript
mode: command
"""

# fmt: off

ctx.lists["user.code_data_type"] = {
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
}

ctx.lists["user.code_collection_type"] = {
    "list"      : "Array",
    "array"     : "Array",
    "record"    : "Record",
    "partial"   : "Partial",
    "omit"      : "Omit",
    "required"  : "Required",
    "pick"      : "Pick",
    "map"       : "Map",
    "set"       : "Set",
}

ctx.lists["user.code_function_modifier"] = {
    "public"    : "public",
    "private"   : "private",
    "protected" : "protected",
}

ctx.lists["user.code_keyword"] = {
    **js_keywords,
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

    def code_format_collection_type(collection_type: str, item_types: list[str]) -> str:
        if item_types:
            return f"{collection_type}<{', '.join(item_types)}>"
        return collection_type

    def code_format_array_type(item_type: str) -> str:
        if " " in item_type:
            item_type = f"({item_type})"
        return f"{item_type}[]"

    def code_format_or_type(item_types: list[str]) -> str:
        return f"{' | '.join(item_types)}"
