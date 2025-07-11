from talon import Module, Context, actions
from ..tags.code_operators import CodeOperators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: java
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

abstract = {"abstract"}
final = {"final"}
static = {"static"}

all_keywords = {
    *access_modifiers,
    *abstract,
    *final,
    *static,
}

ctx.lists["user.code_class_modifier"] = {*access_modifiers, *abstract, *final}

ctx.lists["user.code_function_modifier"] = {
    *access_modifiers,
    *abstract,
    *final,
    *static,
}

ctx.lists["user.code_variable_modifier"] = {*access_modifiers, *final, *static}
code_data_type_simple = {
    "int",
    "long",
    "short",
    "char",
    "byte",
    "float",
    "double",
    "String",
    "Map",
    "List",
    "Set",
    "Object",
    "void"
}

ctx.lists["user.code_data_type"] = {
    **{t: t for t in code_data_type_simple},
    "bool"       : "boolean",
    "bite"       : "byte",
}

ctx.lists["user.code_collection_type"] = {
    "list"            : "List",
    "set"             : "Set",
    "map"             : "Map",
    "array list"      : "ArrayList",
    "hash set"        : "HashSet",
    "hash map"        : "HashMap",
    "linked hash map" : "LinkedHashMap"
}

ctx.lists["user.code_call_function"] = {
    "to string"  : "toString",
    "equals"     : "equals",
}

ctx.lists["user.code_keyword"] = {
    **{k: f"{k} " for k in all_keywords},
    "true"        : "true",
    "false"       : "false",
    "null"        : "null",
    "this"        : "this",
    "import"      : "import ",
    "new"         : "new ",
    "return"      : "return ",
    "extends"     : "extends ",
    "implements"  : "implements ",
    "class"       : "class ",
    "void"        : "void ",
    "throw"       : "throw ",
    "instance of" : " instanceof ",
    "continue"    : "continue;",
    "break"       : "break;",
}

# fmt: on


@ctx.action_class("user")
class UserActions:
    # Miscellaneous statements
    def insert_arrow():
        actions.insert(" -> ")

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
                "name": "main",
                "modifiers": "public static",
                "1": "final String[] args",
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
