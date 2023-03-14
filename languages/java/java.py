from talon import Module, Context, actions
from ...merge import merge

insert = actions.insert
insert_snippet = actions.user.insert_snippet

mod = Module()
ctx = Context()

ctx.matches = r"""
tag: user.java
"""

access_modifiers = {"public", "private", "protected"}
abstract = {"abstract"}
final = {"final"}
static = {"static"}
all_keywords = {
    *access_modifiers,
    *abstract,
    *final,
    *static,
}
ctx.lists["self.code_class_modifier"] = {*access_modifiers, *abstract, *final}
ctx.lists["self.code_function_modifier"] = {
    *access_modifiers,
    *abstract,
    *final,
    *static,
}
ctx.lists["self.code_variable_modifier"] = {*access_modifiers, *final, *static}
ctx.lists["self.code_data_type"] = merge(
    {
        "int",
        "long",
        "short",
        "char",
        "byte",
        "float",
        "double",
        "String",
        "Map",
        "List",
        "Set",
        "Object",
    },
    {
        "bool": "boolean",
        "array list": "ArrayList",
        "hash set": "HashSet",
        "hash map": "HashMap",
    },
)
ctx.lists["self.code_function"] = {"toString"}
ctx.lists["self.code_insert"] = merge(
    {k: f"{k} " for k in all_keywords},
    {"null", "this"},
    {
        "import": "import ",
        "new": "new ",
        "extends": "extends ",
        "implements": "implements ",
        "class": "class ",
        "void": "void ",
        "throw": "throw ",
    },
)
ctx.lists["self.code_snippet"] = {
    "arrow function": """() -> {
        \t$0
    }""",
    "finally": """finally {
        \t$0
    }""",
}


@ctx.action_class("user")
class UserActions:
    # Math operators
    def op_exp():
        actions.skip()

    # Selection statements
    def code_catch():
        insert_snippet(
            """catch(Exception ex) {
                \t$0
            }"""
        )

    def code_try_catch():
        insert_snippet(
            """try {
                \t$1
            }
            catch(Exception ex) {
                \t$0
            }"""
        )

    # Iteration statements
    def code_for():
        insert_snippet(
            """for (int i = 0; i < $1; ++i) {
                \t$0
            }"""
        )

    def code_foreach():
        insert_snippet(
            """for (final $1 : $2) {
                \t$0
            }"""
        )

    # Miscellaneous statements
    def insert_arrow():
        insert(" -> ")

    def code_print(text: str = None):
        if text:
            insert(f'System.out.println("{text}");')
        else:
            insert_snippet("System.out.println($0);")

    def code_format_string():
        insert_snippet("String.format(\"$0\")")

    # Class declaration
    def code_class(name: str, modifiers: list[str]):
        text = f"class {name} {{\n\t$0\n}}"
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
        else:
            text = f"public {text}"
        insert_snippet(text)

    # Constructor declaration
    def code_constructor(modifiers: list[str]):
        name = actions.user.vscode_get("andreas.getClassName")
        if not name:
            return
        if modifiers:
            text = f"{' '.join(modifiers)} {name}"
        else:
            text = f"public {name}"
        snip_func(text)

    # Function declaration
    def code_function(name: str, modifiers: list[str]):
        text = f"void {name}"
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
        snip_func(text)

    def code_function_main():
        snip_func("public static void main", "String[] args")

    # Variable declaration
    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        text = name
        if data_type:
            text = f"{data_type} {text}"
        if modifiers:
            text = f"{' '.join(modifiers)} {text}"
        if assign:
            text = text + " = "
        insert(text)


def snip_func(name, args=""):
    if not args:
        args = "$1"
    insert_snippet(
        f"""{name}({args}) {{
            \t$0
        }}"""
    )
