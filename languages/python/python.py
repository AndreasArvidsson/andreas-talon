from talon import Module, Context, actions
from ...merge import merge

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.python
"""

access_modifiers = {"public": "", "protected": "_", "private": "__"}
ctx.lists["self.code_class_modifier"] = {}
ctx.lists["self.code_function_modifier"] = access_modifiers
ctx.lists["self.code_variable_modifier"] = {**access_modifiers, "global": "global"}
ctx.lists["self.code_data_type"] = {
    "string": "str",
    "int": "int",
    "float": "float",
    "complex": "complex",
    "bool": "bool",
    "dict": "dict",
    "set": "set",
    "list": "list",
    "tuple": "tuple",
    "range": "range",
    "none": "None",
    "any": "Any",
    "tuple": "Tuple",
    "union": "Union",
    "optional": "Optional",
}
ctx.lists["self.code_function"] = {
    "format",
    "strip",
    "lstrip",
    "rstrip",
    "replace",
    "split",
    "len",
    "type",
    "range",
    "find",
    "join",
    "sorted",
    "filter",
    "dir",
    "isinstance",
    "enumerate",
}
ctx.lists["self.code_insert"] = merge(
    {"None", "self"},
    {
        "from": "from ",
        "import": "import ",
        "regex": "re",
        "def": "def ",
        "class": "class ",
        "lambda": "lambda: ",
        "global": "global ",
        "pass": "pass",
        "raise": "raise ",
    },
)
ctx.lists["self.code_snippet"] = {
    "item": '"$1": $0,',
    "ternary": "$1 if $2 else $0",
    "exception": "Exception($0)",
    "raise exception": "raise Exception($0)",
    "finally": "finally:\n\t$0",
}


@ctx.action_class("user")
class UserActions:
    # Assignment operator
    def op_assign():
        actions.insert(" = ")

    # Math operators
    def op_sub():
        actions.insert(" - ")

    def op_sub_assign():
        actions.insert(" -= ")

    def op_add():
        actions.insert(" + ")

    def op_add_assign():
        actions.insert(" += ")

    def op_mult():
        actions.insert(" * ")

    def op_mult_assign():
        actions.insert(" *= ")

    def op_div():
        actions.insert(" / ")

    def op_div_assign():
        actions.insert(" /= ")

    def op_mod():
        actions.insert(" % ")

    def op_mod_assign():
        actions.insert(" %= ")

    def op_exp():
        actions.insert(" ** ")

    # Comparison operators
    def op_equal():
        actions.insert(" == ")

    def op_not_equal():
        actions.insert(" != ")

    def op_less():
        actions.insert(" < ")

    def op_greater():
        actions.insert(" > ")

    def op_less_or_eq():
        actions.insert(" <= ")

    def op_greater_or_eq():
        actions.insert(" >= ")

    def op_not():
        actions.insert("not ")

    def op_equal_null():
        actions.insert(" is None")

    def op_not_equal_null():
        actions.insert(" is not None")

    # Logical operators
    def op_and():
        actions.insert(" and ")

    def op_or():
        actions.insert(" or ")

    # Comments
    def comments_insert(text: str = ""):
        actions.insert(f"# {text}")

    def comments_insert_block(text: str = ""):
        actions.insert_snippet(f'"""{text}$0"""')

    def comments_insert_docstring(text: str = ""):
        actions.user.comments_insert_block(text)

    # Selection statements
    def code_if():
        actions.insert_snippet("if $1:\n\t$0")

    def code_elif():
        actions.insert_snippet("elif $1:\n\t$0")

    def code_else():
        actions.insert_snippet("else:\n\t$0")

    def code_try():
        actions.insert_snippet(
            """try:
                \t$0"""
        )

    def code_catch():
        actions.insert_snippet(
            """except:
                \t$0"""
        )

    def code_try_catch():
        actions.insert_snippet(
            """try:
                \t$1
            except Exception as ex:
                \t$0"""
        )

    # Iteration statements
    def code_for():
        actions.insert_snippet(
            """for i in range($1):
                \t$0"""
        )

    def code_foreach():
        actions.insert_snippet(
            """for $1 in $2:
                \t$0"""
        )

    def code_while():
        actions.insert_snippet(
            """while $1:
                \t$0"""
        )

    # Miscellaneous statements
    def code_break():
        actions.insert("break")

    def code_true():
        actions.insert("True")

    def code_false():
        actions.insert("False")

    def code_continue():
        actions.insert("continue")

    def code_return():
        actions.insert("return ")

    def insert_arrow():
        actions.insert(" -> ")

    def code_print(text: str = None):
        if text:
            actions.insert(f'print("{text}")')
        else:
            actions.insert_snippet("print($0)")

    def code_format_string():
        actions.insert_snippet('f"$0"')

    # Class statement
    def code_class(name: str, modifiers: list[str]):
        actions.insert_snippet(
            f"""class {name}:
                \t$0"""
        )

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        actions.insert_snippet(
            """def __init__(self$1):
                \t$0"""
        )

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        actions.insert_snippet(
            f"""def {''.join(modifiers)}{name}($1):
                \t$0"""
        )

    # Variable statement
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
        if data_type:
            text = f"{text}: {data_type}"
        if assign:
            text += " = "
        actions.insert(text)

    # Function call
    def code_call_function(name: str):
        actions.insert_snippet(f"{name}($TM_SELECTED_TEXT$0)")

    # Insert types
    def code_insert_type_annotation(type: str):
        actions.insert(f": {type}")

    def code_insert_return_type(type: str):
        actions.insert(f" -> {type}")

    # Formatting getters
    def code_get_class_format() -> str:
        return "PASCAL_CASE"

    def code_get_function_format() -> str:
        return "SNAKE_CASE"

    def code_get_variable_format() -> str:
        return "SNAKE_CASE"
