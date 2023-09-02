from talon import Module, Context, actions

mod = Module()
ctx = Context()

ctx.matches = r"""
code.language: python
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
    "range": "range",
    "none": "None",
    "any": "Any",
    "tuple": "tuple",
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
ctx.lists["self.code_insert"] = {
    "true": "True",
    "false": "False",
    "None": "None",
    "self": "self",
    "pass": "pass",
    "from": "from ",
    "regex": "re",
    "return": "return ",
    "import": "import ",
    "def": "def ",
    "class": "class ",
    "lambda": "lambda: ",
    "global": "global ",
    "raise": "raise ",
    "yield": "yield ",
    "break": "break",
    "exception": "Exception",
    "continue": "continue",
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

    # Miscellaneous statements

    def insert_arrow():
        actions.insert(" -> ")

    # Class statement
    def code_class(name: str, modifiers: list[str]):
        actions.user.code_insert_snippet("classDeclaration", {"name": name})

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        actions.user.code_insert_snippet("constructorDeclaration")

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        actions.user.code_insert_snippet(
            "functionDeclaration",
            {"name": f"{''.join(modifiers)}{name}"},
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
