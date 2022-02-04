from talon import Module, Context, actions
from ...merge import merge

insert = actions.insert
insert_snippet = actions.user.insert_snippet

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.javascript
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
        "import": "import ",
        "export": "export ",
        "export default": "export default ",
        "default": "default ",
        "extends": "extends ",
        "implements": "implements ",
        "async": "async ",
        "await": "await ",
        "function": "function ",
        "default": "default ",
        "spread": "...",
        "new": "new ",
        "const": "const ",
        "let": "let ",
        "throw": "throw ",
        "static": "static ",
    },
)
ctx.lists["self.code_insert"] = javascript_inserts
ctx.lists["self.code_snippet"] = {
    "item": "$1: $0,",
    "for in loop": """for (const $1 in $2) {
        \t$0
    }""",
    "arrow function": """($1) => {
        \t$0
    }""",
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
            """catch(ex) {
                \t$0
            }"""
        )

    def code_try_catch():
        insert_snippet(
            """try {
                \t$1
            }
            catch(ex) {
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
