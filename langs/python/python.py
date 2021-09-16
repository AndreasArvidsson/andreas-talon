from talon import Module, Context, actions
from ....andreas.merge import merge

key = actions.key
insert = actions.insert
mod = Module()
ctx = Context()

ctx.matches = r"""
mode: user.python
mode: user.auto_lang
and code.language: python
"""

ctx.lists["self.code_data_type"] = {
    "int":      "int",
    "bool":     "bool",
    "string":   "str",
    "dict":     "dict",
    "list":     "list",
    "tuple":    "tuple"
}
ctx.lists["self.code_access_modifier"] = {
    "global"
}
ctx.lists["self.code_member_op"] = {
    "dot": "."
}
ctx.lists["self.code_function"] = {
    "format", "strip", "lstrip", "rstrip", "replace", "split",
    "len", "type", "range"
}
ctx.lists["self.code_member"] = {

}
ctx.lists["self.code_statement"] = merge(
    {
        "self", "None", "zip"
    },
    {
        "from":             "from ",
        "import":           "import ",
        "lambda":           "lambda ",
        "arrow":            " -> ",
        "self dot":         "self.",
        "string":           "str",
        "regexp":           "re",
        "def":              "def "
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

    # Logical operators
    def op_and():               insert(" and ")
    def op_or():                insert(" or ")

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
    def code_comment(): insert("# ")

    def code_block_comment():
        insert('""""""')
        key("left:3")

    def code_print(text: str = None):
        if text:
            insert(f'print("{text}")')
        else:
            insert("print()")
            key("left")

    # Class statement
    def code_class(access_modifier: str or None, name: str):
        insert("class {}:".format(name))
        actions.edit.line_insert_down()

    # Constructor statement
    def code_constructor(access_modifier: str):
        insert("def __init__(self):")
        key("left:2")

    # Function statement
    def code_function(access_modifier: str or None, name: str):
        insert(f"def {name}():")
        key("left:2")

    # Variable statement
    def code_variable(access_modifier: str or None, data_type: str or None, name: str, assign: str or None):
        if data_type:
            text = f"{data_type} {name}"
        else:
            text = name
        if assign:
            text = text + " = "
        insert(text)

    # Function call
    def code_call_function(name: str):
        insert(f"{name}()")
        key("left")

    # Member access
    def code_member_access(operator: str, name: str):
        insert(f"{operator}{name}")

    # Formatting getters
    def code_get_class_format() -> str: return "PASCAL_CASE"
    def code_get_function_format() -> str: return "SNAKE_CASE"
    def code_get_variable_format() -> str: return "SNAKE_CASE"
