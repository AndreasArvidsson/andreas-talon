from talon import Module, Context, actions
from ...merge import merge

insert = actions.insert
insert_snippet = actions.user.insert_snippet

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
    },
)
ctx.lists["self.code_snippet"] = {
    "item": '"$1": $0,',
}


@ctx.action_class("user")
class UserActions:
    # Assignment operator
    def op_assign():
        insert(" = ")

    # Math operators
    def op_sub():
        insert(" - ")

    def op_sub_assign():
        insert(" -= ")

    def op_add():
        insert(" + ")

    def op_add_assign():
        insert(" += ")

    def op_mult():
        insert(" * ")

    def op_mult_assign():
        insert(" *= ")

    def op_div():
        insert(" / ")

    def op_div_assign():
        insert(" /= ")

    def op_mod():
        insert(" % ")

    def op_mod_assign():
        insert(" %= ")

    def op_exp():
        insert(" ** ")

    # Comparison operators
    def op_equal():
        insert(" == ")

    def op_not_equal():
        insert(" != ")

    def op_less():
        insert(" < ")

    def op_greater():
        insert(" > ")

    def op_less_or_eq():
        insert(" <= ")

    def op_greater_or_eq():
        insert(" >= ")

    def op_not():
        insert("not ")

    def op_equal_null():
        insert(" is None")

    def op_not_equal_null():
        insert(" is not None")

    # Logical operators
    def op_and():
        insert(" and ")

    def op_or():
        insert(" or ")

    # Comments
    def comments_insert(text: str = ""):
        insert(f"# {text}")

    def comments_insert_block(text: str = ""):
        insert_snippet(f'"""{text}$0"""')

    # Selection statements
    def code_if():
        insert("if ")

    def code_elif():
        insert("elif ")

    def code_else():
        insert("else:")

    def code_try():
        insert_snippet(
            """try:
                \t$0"""
        )

    def code_catch():
        insert_snippet(
            """except:
                \t$0"""
        )

    def code_try_catch():
        insert_snippet(
            """try:
                \t$1
            except:
                \t$0"""
        )

    # Iteration statements
    def code_for():
        insert_snippet(
            """for i in range($1):
                \t$0"""
        )

    def code_foreach():
        insert_snippet(
            """for $1 in $2:
                \t$0"""
        )

    def code_while():
        insert_snippet(
            """while $1:
                \t$0"""
        )

    # Miscellaneous statements
    def code_break():
        insert("break")

    def code_true():
        insert("True")

    def code_false():
        insert("False")

    def code_continue():
        insert("continue")

    def code_return():
        insert("return ")

    def insert_arrow():
        insert(" -> ")

    def code_print(text: str = None):
        if text:
            insert(f'print("{text}")')
        else:
            insert_snippet("print($0)")

    def code_format_string():
        insert_snippet('f"$0"')

    # Class statement
    def code_class(name: str, modifiers: list[str]):
        insert_snippet(
            f"""class {name}:
                \t$0"""
        )

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        insert_snippet(
            """def __init__(self$1):
                \t$0"""
        )

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        insert_snippet(
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
            text = text + " = "
        insert(text)

    # Function call
    def code_call_function(name: str):
        insert_snippet(f"{name}($0)")

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
