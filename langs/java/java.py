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
ctx.lists["self.code_statement"] = merge(
    {k: f"{k} " for k in all_keywords},
    {"null", "this"},
    {
        "import": "import ",
        "new": "new ",
        "extends": "extends ",
        "implements": "implements ",
    },
)


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
        actions.skip()

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
        insert("!")

    def op_equal_null():
        insert(" == null")

    def op_not_equal_null():
        insert(" != null")

    # Logical operators
    def op_and():
        insert(" && ")

    def op_or():
        insert(" || ")

    # Comments
    def comments_insert(text: str = ""):
        insert(f"// {text}")

    def comments_insert_block(text: str = ""):
        insert_snippet(f"/* {text}$0 */")

    # Selection statements
    def code_if():
        snip_func("if")

    def code_elif():
        snip_func("else if")

    def code_else():
        insert_snippet(
            """else {
                \t$0
            }"""
        )

    def code_switch():
        snip_func("switch")

    def code_case():
        insert("case ")

    def code_default():
        insert("default:")

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

    def code_while():
        snip_func("while")

    def code_do_while():
        insert_snippet(
            """do {
                \t$0
            } while ($1);"""
        )

    # Miscellaneous statements
    def code_break():
        insert("break;")

    def code_true():
        insert("true")

    def code_false():
        insert("false")

    def code_continue():
        insert("continue;")

    def code_return():
        insert("return")

    def insert_arrow():
        insert(" -> ")

    def code_print(text: str = None):
        if text:
            insert(f'System.out.println("{text}");')
        else:
            insert_snippet("System.out.println($0);")

    def code_format_string():
        insert_snippet("String.format($0)")

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
        name = actions.user.vscode_get("andreas.constructorName")
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

    # Function call
    def code_call_function(name: str):
        insert_snippet(f"{name}($0)")

    # Formatting getters
    def code_get_class_format() -> str:
        return "PASCAL_CASE"

    def code_get_function_format() -> str:
        return "CAMEL_CASE"

    def code_get_variable_format() -> str:
        return "CAMEL_CASE"


def snip_func(name, args=""):
    if not args:
        args = "$1"
    insert_snippet(
        f"""{name}({args}) {{
            \t$0
        }}"""
    )
