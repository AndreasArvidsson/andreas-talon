from talon import Module, Context, actions

mod = Module()

ctx = Context()
ctx.matches = r"""
code.language: javascript
code.language: typescript
code.language: javascriptreact
code.language: typescriptreact
"""

ctx.lists["self.code_class_modifier"] = {}
ctx.lists["self.code_function_modifier"] = {}
ctx.lists["self.code_variable_modifier"] = {
    "const",
    "let",
}
ctx.lists["self.code_data_type"] = {}
ctx.lists["self.code_function"] = {
    "forEach",
    "map",
    "flatMap",
    "filter",
    "reduce",
    "sort",
    "find",
    "includes",
    "indexOf",
    "join",
    "require",
}
javascript_inserts = {
    "true": "true",
    "false": "false",
    "null": "null",
    "undefined": "undefined",
    "this": "this",
    "from": " from ",
    "import": "import ",
    "export": "export ",
    "default": "default ",
    "extends": " extends ",
    "abstract": "abstract ",
    "implements": "implements ",
    "return": "return ",
    "a sync": "async ",
    "await": "await ",
    "function": "function ",
    "spread": "...",
    "new": "new ",
    "const": "const ",
    "let": "let ",
    "throw": "throw ",
    "static": "static ",
    "get": "get ",
    "set": "set ",
    "nullish": " ?? ",
    "instance of": " instanceof ",
    "type of": "typeof ",
    "yield": "yield ",
    "delete": "delete ",
    "continue": "continue;",
    "break": "break;",
}

ctx.lists["self.code_insert"] = javascript_inserts


@ctx.action_class("user")
class UserActions:
    # Math operators
    def op_exp():
        actions.insert(" ** ")

    # Comparison operators
    def op_equal():
        actions.insert(" === ")

    def op_not_equal():
        actions.insert(" !== ")

    # Class statement
    def code_class(name: str, modifiers: list[str]):
        actions.user.code_insert_snippet("classDeclaration", {"name": name})

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        actions.user.code_insert_snippet("constructorDeclaration")

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        actions.user.code_insert_snippet("functionDeclaration", {"name": name})

    def code_method(name: str, modifiers: list[str]):
        actions.user.code_insert_snippet("methodDeclaration", {"name": name})

    # Variable statement
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
            if "const" in modifiers:
                assign = True
        if data_type:
            text = f"{text}: {data_type}"
        if assign:
            text += " = "
        actions.insert(text)


@mod.action_class
class Actions:
    def js_arrowify_line():
        """Arrowify line"""
        actions.edit.select_line()
        text = actions.edit.selected_text()
        if "function" in text:
            text = text.replace("function ", "")
        text = f"const {text}"
        text = text.replace("(", " = (")
        text = text.replace(")", ") =>")
        actions.insert(text)

    def js_arrow_function(name: str):
        """Insert arrow function"""
        format = actions.user.code_get_function_format()
        name = actions.user.format_text(name, format)
        actions.user.code_insert_snippet("namedLambdaExpression", {"name": name})
