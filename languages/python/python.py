from talon import Context, Module, actions
from ..tags.code_operators import CodeOperators

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: python
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
    op_pow           = " ** ",
    is_equal         = " == ",
    is_not_equal     = " != ",
    is_less          = " < ",
    is_greater       = " > ",
    is_less_equal    = " <= ",
    is_greater_equal = " >= ",
    is_not           = "not ",
    is_null          = " is None",
    is_not_null      = " is not None",
    is_in            = " in ",
    op_in            = " in ",
    op_and           = " and ",
    op_or            = " or ",
)

access_modifiers = {
    "public": "",
    "protected": "_",
    "private": "__",
}

ctx.lists["user.code_class_modifier"] = {}

ctx.lists["user.code_function_modifier"] = access_modifiers

ctx.lists["user.code_variable_modifier"] = {
    **access_modifiers,
    "global": "global",
}

ctx.lists["user.code_data_type"] = {
    "string"   : "str",
    "int"      : "int",
    "float"    : "float",
    "bool"     : "bool",
    "range"    : "range",
    "none"     : "None",
    "any"      : "Any",
    "complex"  : "complex",
}

ctx.lists["user.code_collection_type"] = {
    "dict"     : "dict",
    "set"      : "set",
    "list"     : "list",
    "tuple"    : "Tuple",
    "union"    : "Union",
    "optional" : "Optional",
}

ctx.lists["user.code_call_function"] = {
    "format"      : "format",
    "strip"       : "strip",
    "replace"     : "replace",
    "split"       : "split",
    "type"        : "type",
    "range"       : "range",
    "find"        : "find",
    "join"        : "join",
    "sorted"      : "sorted",
    "filter"      : "filter",
    "dir"         : "dir",
    "is instance" : "isinstance",
    "enumerate"   : "enumerate",
    "list"        : "list",
    "set"         : "set",
    "string"      : "str",
    "length"      : "len",
    "left strip"  : "lstrip",
    "right strip" : "rstrip",
    "update"      : "update",
    "append"      : "append",
}

ctx.lists["user.code_keyword"] = {
    "true"      : "True",
    "false"     : "False",
    "None"      : "None",
    "self"      : "self",
    "pass"      : "pass",
    "from"      : "from ",
    "regex"     : "re",
    "return"    : "return ",
    "import"    : "import ",
    "def"""       : "def ",
    "class"     : "class ",
    "lambda"    : "lambda: ",
    "global"    : "global ",
    "race"      : "raise ",
    "yield"     : "yield ",
    "break"     : "break",
    "exception" : "Exception",
    "continue"  : "continue",
}

# fmt: on


@ctx.action_class("user")
class UserActions:
    # Class statement
    def code_class(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name("classDeclaration", {"name": name})

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        actions.user.insert_snippet_by_name("constructorDeclaration")

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        actions.user.insert_snippet_by_name(
            "functionDeclaration",
            {"name": f"{''.join(modifiers)}{name}"},
        )

    # Variable statement
    def code_variable(assign: bool, modifiers: list[str], data_type: str, name: str):
        snippet = ""
        if modifiers:
            snippet = f"{' '.join(modifiers)} "
        snippet += name or "$1"
        if data_type:
            snippet += f": {data_type}"
        if assign:
            snippet += " =  $0"
        actions.user.insert_snippet(snippet)

    # Insert types
    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" -> {type}")

    def code_format_collection_type(collection_type: str, item_types: list[str]) -> str:
        if item_types:
            return f"{collection_type}[{', '.join(item_types)}]"
        return collection_type

    def code_format_array_type(item_type: str) -> str:
        return actions.user.code_format_collection_type("list", [item_type])

    def code_format_or_type(item_types: list[str]) -> str:
        return f"{' | '.join(item_types)}"
