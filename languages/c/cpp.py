from talon import Module, Context, actions
from .c import c_code_data_type_simple, c_keywords

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: cpp
# Make typescript win over C
mode: command
"""

ctx.lists["user.code_data_type"] = {
    **c_code_data_type_simple,
    "string": "string",
}

ctx.lists["user.code_collection_type"] = {
    "vector": "vector",
    "map": "map",
    "set": "set",
    "unordered map": "unordered_map",
    "unordered set": "unordered_set",
}


ctx.lists["user.code_keyword"] = {
    **c_keywords,
    "this": "this",
    "include": "#include ",
    "new": "new ",
    "class": "class ",
    "throw": "throw ",
}


@ctx.action_class("user")
class UserActions:
    def code_constructor():
        actions.user.code_constructor_with_class_name()
