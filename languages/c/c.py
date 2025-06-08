from talon import Module, Context, actions
from ..tags.code_operators import CodeOperators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: c
code.language: cpp
"""

# fmt: off

ctx.lists["user.code_operator"] = CodeOperators(
    op_assign        = " = ",
    op_sub           = " - ",
    op_sub_assign    = " -= ",
    op_add           = " + ",
    op_add_assign    = " += ",
    op_mult          = " * ",
    op_mult_assign   = " *= ",
    op_div           = " / ",
    op_div_assign    = " /= ",
    op_mod           = " % ",
    op_mod_assign    = " %= ",
    is_equal         = " == ",
    is_not_equal     = " != ",
    is_less          = " < ",
    is_greater       = " > ",
    is_less_equal    = " <= ",
    is_greater_equal = " >= ",
    is_not           = "!",
    is_null          = " == null",
    is_not_null      = " != null",
    op_and           = " && ",
    op_or            = " || ",
)

ctx.lists["user.code_class_modifier"] = {}

ctx.lists["user.code_function_modifier"] = {}

ctx.lists["user.code_variable_modifier"] = {}

code_data_type_simple = {
    "int",
    "long",
    "short",
    "char",
    "byte",
    "float",
    "double",
    "void"
}

c_code_data_type_simple = {
    **{t: t for t in code_data_type_simple},
    "bool"       : "bool",
    "bite"       : "byte",
}

ctx.lists["user.code_data_type"] = c_code_data_type_simple

ctx.lists["user.code_collection_type"] = {}

ctx.lists["user.code_call_function"] = {}

c_code_insert={
    "true"        : "true",
    "false"       : "false",
    "null"        : "null",
    "return"      : "return ",
    "void"        : "void ",
    "continue"    : "continue;",
    "break"       : "break;",
}

ctx.lists["user.code_insert"] = c_code_insert

# fmt: on


@ctx.action_class("user")
class UserActions:
    # Miscellaneous statements
    def insert_arrow():
        actions.insert(" -> ")

    # Function declaration
    def code_function(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name(
            "functionDeclaration",
            {"name": name},
        )

    def code_function_main():
        actions.user.insert_snippet_by_name(
            "functionDeclaration",
            {
                "name": "main",
                "1": "int argc, char *argv[]",
            },
        )

    # Variable declaration
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if data_type:
            text = f"{data_type} {text}"
        if assign:
            text += " = "
        actions.insert(text)
