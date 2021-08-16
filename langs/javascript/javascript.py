from talon import Module, Context, actions
key = actions.key
insert = actions.insert
mod = Module()
ctx = Context()

ctx.matches = r"""
mode: user.javascript
mode: user.auto_lang
and code.language: javascript
mode: user.typescript
mode: user.auto_lang
and code.language: typescript
"""

ctx.lists["self.code_data_type"] = {
    "let", "const"
}
ctx.lists["self.code_member_op"] = {
    "dot": "."
}
ctx.lists["self.code_function"] = {
    "forEach", "map", "flatMap", "filter", "reduce",
    "sort", "find", "includes", "indexOf",
    "join", "require"
}
ctx.lists["self.code_member"] = {
    "length"
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
    "new":                  "new ",
    "const":                "const ",
    "let":                  "let ",
    "bool":                 "boolean",
    "number":               "number"
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

    # Boolean operators
    def op_and():               insert(" && ")
    def op_or():                insert(" || ")
    def op_equal():             insert(" === ")
    def op_not_equal():         insert(" !== ")
    def op_less():              insert(" < ")
    def op_greater():           insert(" > ")
    def op_less_or_eq():        insert(" <= ")
    def op_greater_or_eq():     insert(" >= ")
    def op_not():               insert("!")

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
    def code_comment():         insert("// ")

    def code_block_comment():
        insert("/*\n\n*/")
        key("up")

    def code_print(text: str = None):
        if text:
            insert(f'console.log("{text}");')
        else:
            insert("console.log();")
            key("left:2")

    # Class statement
    def code_class(access_modifier: str or None, name: str):
        insert(f"class {name} {{}}")
        key("left enter")

    # Constructor statement
    def code_constructor(access_modifier: str):
        snip_func("constructor")

    # Function statement
    def code_function(access_modifier: str or None, name: str):
        snip_func(f"function {name}")

    # Variable statement
    def code_variable(access_modifier: str or None, data_type: str or None, name: str, assign: str or None):
        if data_type:
            text = f"{data_type} {name}"
        else:
            text = name
        if assign:
            text = text + " = "
        insert(text)

    # Function called
    def code_call_function(name: str):
        insert(f"{name}()")
        key("left")

    # Member access
    def code_member_access(operator: str, name: str):
        insert(f"{operator}{name}")

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
