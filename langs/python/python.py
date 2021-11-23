from talon import Module, Context, actions
from ....andreas.merge import merge

key = actions.key
insert = actions.insert
mod = Module()
ctx = Context()

ctx.matches = r"""
mode: command
and mode: user.python

mode: command
and mode: user.auto_lang
and code.language: python
"""

access_modifiers = {
    "public":       "",
    "protected":    "_",
    "private":      "__"
}
ctx.lists["self.code_class_modifier"] = {}
ctx.lists["self.code_function_modifier"] = access_modifiers
ctx.lists["self.code_variable_modifier"] = {
    **access_modifiers,
    "global": "global"
}
ctx.lists["self.code_data_type"] = {
    "string":   "str",
    "int":      "int",
    "float":    "float",
    "complex":  "complex",
    "bool":     "bool",
    "dict":     "dict",
    "set":      "set",
    "list":     "list",
    "tuple":    "tuple",
    "range":    "range"
}
ctx.lists["self.code_function"] = {
    "format", "strip", "lstrip", "rstrip", "replace", "split",
    "len", "type", "range", "find", "join"
}
ctx.lists["self.code_statement"] = merge(
    {
        "None", "self", "lambda"
    },
    {
        "from":             "from ",
        "import":           "import ",
        "arrow":            " -> ",
        "regex":            "re",
        "def":              "def ",
        "class":            "class ",
        "try":              "try:",
        "except":           "except:",
    }
)


@ctx.action_class("user")
class UserActions:
    # Assignment operator
    def op_assign():            insert(" = ")
    # Math operators
    def op_sub():               insert(" - ")
    def op_sub_assign():        insert(" -= ")
    def op_add():               insert(" + ")
    def op_add_assign():        insert(" += ")
    def op_mult():              insert(" * ")
    def op_mult_assign():       insert(" *= ")
    def op_div():               insert(" / ")
    def op_div_assign():        insert(" /= ")
    def op_mod():               insert(" % ")
    def op_mod_assign():        insert(" %= ")
    def op_exp():               insert(" ** ")
    # Comparison operators
    def op_equal():             insert(" == ")
    def op_not_equal():         insert(" != ")
    def op_less():              insert(" < ")
    def op_greater():           insert(" > ")
    def op_less_or_eq():        insert(" <= ")
    def op_greater_or_eq():     insert(" >= ")
    def op_not():               insert("not ")
    def op_equal_null():        insert(" is None")
    def op_not_equal_null():    insert(" is not None")
    # Logical operators
    def op_and():               insert(" and ")
    def op_or():                insert(" or ")

    # Comments
    def comments_insert(text: str = ""):
        insert(f"# {text}")

    def comments_insert_block(text: str = ""):
        insert(f"\"\"\"{text}\"\"\"")
        key("left:3")

    # Selection statements
    def code_if():      insert("if ")
    def code_elif():    insert("elif ")
    def code_else():    insert("else:")

    # Iteration statements
    def code_for():
        insert("for i in range():")
        key("left:2")

    def code_while():
        insert("while ():")
        key("left:2")

    def code_do_while():
        insert("do {\n\n} while ()\n")
        key("left:2")

    def code_foreach():
        insert("for  in :")
        key("left:5")

    # Miscellaneous statements
    def code_break(): insert("break")
    def code_true(): insert("True")
    def code_false(): insert("False")
    def code_continue(): insert("continue")
    def code_return(): insert("return")

    def code_print(text: str = None):
        if text:
            insert(f'print("{text}")')
        else:
            insert("print()")
            key("left")

    def code_format_string():
        insert('f""')
        key("left")

    # Class statement
    def code_class(name: str, modifiers: list[str]):
        insert(f"class {name}:")
        actions.edit.line_insert_down()

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        insert("def __init__(self):")
        key("left:2")

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        insert(f"def {''.join(modifiers)}{name}():")
        key("left:2")

    # Variable statement
    def code_variable(name: str, modifiers: list[str], assign: bool, data_type: str = None):
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
        insert(f"{name}()")
        key("left")

    # Formatting getters
    def code_get_class_format() -> str:     return "PASCAL_CASE"
    def code_get_function_format() -> str:  return "SNAKE_CASE"
    def code_get_variable_format() -> str:  return "SNAKE_CASE"
