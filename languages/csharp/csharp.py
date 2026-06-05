from talon import Context, Module, actions
from ..tags.code_operators import CodeOperators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: csharp
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

access_modifiers = {
    "public":    "public",
    "private":   "private",
    "protected": "protected",
}


ctx.lists["user.code_variable_modifier"] = {
    **access_modifiers,
    "const": "const",
}

code_data_type_simple = {
    "int",
    "long",
    "short",
    "char",
    "byte",
    "float",
    "double",
    "string",
    "bool",
    "void"
}

ctx.lists["user.code_data_type"] = {
    **{t: t for t in code_data_type_simple},
    "bite"       : "byte",
}

ctx.lists["user.code_collection_type"] = {}

ctx.lists["user.code_call_function"] = {}

ctx.lists["user.code_keyword"] = {
    **access_modifiers,
    "static"      : "static",
    "true"        : "true",
    "false"       : "false",
    "null"        : "null",
    "this"        : "this",
    "using"       : "using ",
    "new"         : "new ",
    "return"      : "return ",
    "class"       : "class ",
    "void"        : "void ",
    "throw"       : "throw ",
    "continue"    : "continue;",
    "break"       : "break;",
    "abstract"    : "abstract",
    "sealed"      : "sealed",
}

# fmt: on


@ctx.action_class("user")
class UserActions:
    @staticmethod
    def code_constructor():
        actions.user.code_constructor_with_class_name()

    @staticmethod
    def code_variable(assign: bool, modifiers: list[str], data_type: str, name: str):
        snippet = ""
        if modifiers:
            snippet = f"{' '.join(modifiers)} "
            if "final" in modifiers:
                assign = True
        if not data_type and not name:
            snippet += "$1"
        else:
            snippet += f"{data_type or '$1'} {name or '$1'}"
        if assign:
            snippet += " = $0"
        actions.user.insert_snippet(snippet)
