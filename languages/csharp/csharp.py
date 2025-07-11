from talon import Module, Context, actions
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
    "public",
    "private",
    "protected",
}

static = {"static"}
all_keywords = {
    *access_modifiers,
    *static,
}

ctx.lists["user.code_class_modifier"] = {*access_modifiers}

ctx.lists["user.code_function_modifier"] = {
    *access_modifiers,
    *static,
}

ctx.lists["user.code_variable_modifier"] = {*access_modifiers}
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
    **{k: f"{k} " for k in all_keywords},
    "true"        : "true",
    "false"       : "false",
    "null"        : "null",
    "this"        : "this",
    "using"      : "using ",
    "new"         : "new ",
    "return"      : "return ",
    "class"       : "class ",
    "void"        : "void ",
    "throw"       : "throw ",
    "continue"    : "continue;",
    "break"       : "break;",
}

# fmt: on


@ctx.action_class("user")
class UserActions:
    # Class declaration
    def code_class(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name(
            "classDeclaration",
            {"name": name, "modifiers": get_modifiers(modifiers)},
        )

    # Constructor declaration
    def code_constructor(modifiers: list[str]):
        name = actions.user.code_get_class_name()
        if not name:
            raise ValueError("Class name not found")
        actions.user.insert_snippet_by_name(
            "constructorDeclaration",
            {"name": name, "modifiers": get_modifiers(modifiers)},
        )

    # Function declaration
    def code_function(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name(
            "functionDeclaration",
            {"name": name, "modifiers": get_modifiers(modifiers)},
        )

    def code_function_main():
        actions.user.insert_snippet_by_name(
            "functionDeclaration",
            {
                "name": "Main",
                "modifiers": "static",
                "1": "string[] args",
            },
        )

    # Variable declaration
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if data_type:
            text = f"{data_type} {text}"
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
        if assign:
            text += " = "
        actions.insert(text)


def get_modifiers(modifiers: list[str]):
    if modifiers:
        return " ".join(modifiers)
    else:
        return "public"
