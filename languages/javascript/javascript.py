from talon import Module, Context, actions
from ...merge import merge

insert = actions.insert
insert_snippet = actions.user.insert_snippet

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.javascript
# Make javascript have precedence over c common
mode: command
"""

ctx.lists["self.code_class_modifier"] = {}
ctx.lists["self.code_function_modifier"] = {}
ctx.lists["self.code_variable_modifier"] = {"const", "let"}
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
javascript_inserts = merge(
    {"null", "undefined", "this"},
    {
        "from": " from ",
        "import": "import ",
        "export": "export ",
        "default": "default ",
        "extends": " extends ",
        "abstract": "abstract ",
        "implements": "implements ",
        "async": "async ",
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
    },
)
ctx.lists["self.code_insert"] = javascript_inserts

for_in_loop = """for (const $1 in $2) {
    \t$0
}"""
arrow_function = """($1) => {
    \t$0
}"""

ctx.lists["self.code_snippet"] = {
    "item": "$1: $0,",
    "for in loop": for_in_loop,
    "for in": for_in_loop,
    "arrow function": arrow_function,
    "lambda": arrow_function,
    "self calling": """(() => {
        \t$0
    })();""",
    "error": "throw Error($0)",
    "tertiary": "$1 ? $2 : $0",
    "import star": 'import * as $0 from "$0";',
    "import from": 'import $0 from "$0";',
}


@ctx.action_class("user")
class UserActions:
    # Math operators
    def op_exp():
        insert(" ** ")

    # Comparison operators
    def op_equal():
        insert(" === ")

    def op_not_equal():
        insert(" !== ")

    # Selection statements
    def code_catch():
        insert_snippet(
            """catch(error) {
                \t$0
            }"""
        )

    def code_try_catch():
        insert_snippet(
            """try {
                \t$1
            }
            catch(error) {
                \t$0
            }"""
        )

    # Iteration statements
    def code_for():
        insert_snippet(
            """for (let i = 0; i < $1; ++i) {
                \t$0
            }"""
        )

    def code_foreach():
        insert_snippet(
            """for (const $1 of $2) {
                \t$0
            }"""
        )

    # Miscellaneous statements
    def code_print(text: str = None):
        if text:
            insert(f'console.log("{text}")')
        else:
            insert_snippet("console.log($0)")

    def code_format_string():
        insert_snippet("`$0`")

    # Class statement
    def code_class(name: str, modifiers: list[str]):
        insert_snippet(
            f"""class {name} {{
                \t$0
            }}"""
        )

    # Constructor statement
    def code_constructor(modifiers: list[str]):
        snip_func("constructor")

    # Function statement
    def code_function(name: str, modifiers: list[str]):
        snip_func(f"function {name}")

    def code_method(name: str, modifiers: list[str]):
        snip_func(f"{name}")

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
            text = text + " = "
        insert(text)


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
    insert_snippet(
        f"""{name}($1) {{
            \t$0
        }}"""
    )
