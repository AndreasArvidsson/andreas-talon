from typing import List
from talon import Module, Context, actions
key = actions.key
insert = actions.insert

mod = Module()
mod.tag("javascript")

ctx = Context()
ctx.matches = r"""
mode: command
and mode: user.javascript

mode: command
and mode: user.auto_lang
and code.language: javascript

mode: command
and tag: user.javascript
"""

ctx.lists["self.code_class_modifier"] = {}
ctx.lists["self.code_function_modifier"] = {}
ctx.lists["self.code_variable_modifier"] = {
    "const", "let"
}
ctx.lists["self.code_data_type"] = {
    "bool":     "boolean",
    "number":   "number",
    "string":   "string",
    "any":      "any"
}
ctx.lists["self.code_function"] = {
    "forEach", "map", "flatMap", "filter", "reduce",
    "sort", "find", "includes", "indexOf",
    "join", "require"
}
ctx.lists["self.code_statement"] = {
    "import":               "import ",
    "async":                "async ",
    "await":                "await ",
    "export":               "export ",
    "function":             "function ",
    "default":              "default ",
    "spread":               "...",
    "null":                 "null",
    "undefined":            "undefined",
    "arrow":                " => ",
    "this":                 "this",
    "this dot":             "this.",
    "new":                  "new "
}


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
    def op_equal():             insert(" === ")
    def op_not_equal():         insert(" !== ")
    def op_less():              insert(" < ")
    def op_greater():           insert(" > ")
    def op_less_or_eq():        insert(" <= ")
    def op_greater_or_eq():     insert(" >= ")
    def op_not():               insert("!")
    def op_equal_null():        insert(" == null")
    def op_not_equal_null():    insert(" != null")
    # Logical operators
    def op_and():               insert(" && ")
    def op_or():                insert(" || ")

    # Comments
    def comments_insert(text: str = ""):
        insert(f"// {text}")

    def comments_insert_block(text: str = ""):
        insert(f"/* {text} */")
        key("left:3")

    # Selection statements
    def code_if():
        snip_func("if")

    def code_elif():
        snip_func("else if")

    def code_else():
        insert("else {}")
        key("left enter")

    def code_switch():
        snip_func("switch")

    def code_case():        insert("case ")
    def code_default():     insert("default:")

    # Iteration statements
    def code_for():
        insert("for (let i = 0; i < .length; ++i) {}")
        key("left enter up home right:20")

    def code_while():
        snip_func("while")

    def code_do_while():
        insert("do {} while ();")
        key("left:11 enter down end left:2")

    def code_foreach():
        insert("for (const e of ) {}")
        key("left enter up end left:3")

    # Miscellaneous statements
    def code_break():           insert("break;")
    def code_true():            insert("true")
    def code_false():           insert("false")
    def code_continue():        insert("continue;")
    def code_return():          insert("return")

    def code_print(text: str = None):
        if text:
            insert(f'console.log("{text}");')
        else:
            insert("console.log();")
            key("left:2")

    def code_format_string():
        insert("``")
        key("left")

    # Class statement
    def code_class(name: str, modifiers: List[str]):
        insert(f"class {name} {{}}")
        key("left enter")

    # Constructor statement
    def code_constructor(modifiers: List[str]):
        snip_func("constructor")

    # Function statement
    def code_function(name: str, modifiers: List[str]):
        snip_func(f"function {name}")

    # Variable statement
    def code_variable(name: str, modifiers: List[str], assign: bool, data_type: str = None):
        text = name
        print(text)
        print(modifiers)
        print(data_type)
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
        if data_type:
            text = f"{text}: {data_type}"
        if assign:
            text = text + " = "
        insert(text)

    # Function called
    def code_call_function(name: str):
        insert(f"{name}()")
        key("left")

    # Formatting getters
    def code_get_class_format() -> str: return "PASCAL_CASE"
    def code_get_function_format() -> str: return "CAMEL_CASE"
    def code_get_variable_format() -> str: return "CAMEL_CASE"


@mod.action_class
class Actions:
    def arrowify_line():
        """Arrowify line"""
        actions.edit.select_line()
        text = actions.edit.selected_text()
        if "function" in text:
            text = text.replace("function ", "")
        text = f"const {text}"
        text = text.replace("(", " = (")
        text = text.replace(")", ") =>")
        actions.insert(text)


def snip_func(name):
    insert(f"{name} () {{}}")
    key("left enter up end left:3")
