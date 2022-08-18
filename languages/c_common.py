from talon import Module, Context, actions

insert = actions.insert
insert_snippet = actions.user.insert_snippet

mod = Module()
ctx = Context()

mod.tag("c_common")

ctx.matches = r"""
tag: user.c_common
tag: user.c_common
and tag: user.html # Solve conflict when using react typescript
"""


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

    # Comparison operators
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

    # Comparison operators
    def op_equal():
        insert(" == ")

    def op_not_equal():
        insert(" != ")

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

    def comments_insert_docstring(text: str = ""):
        insert_snippet(f"/** {text}$0 */")

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
        insert_snippet(
            """case $1:
                \t$0"""
        )

    def code_default():
        insert_snippet(
            """default:
                \t$0"""
        )

    def code_try():
        insert_snippet(
            """try {
                \t$0
            }"""
        )

    # Iteration statements
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
        insert("return ")

    # Function called
    def code_call_function(name: str):
        insert_snippet(f"{name}($0)")

    # Formatting getters
    def code_get_class_format() -> str:
        return "PASCAL_CASE"

    def code_get_function_format() -> str:
        return "CAMEL_CASE"

    def code_get_variable_format() -> str:
        return "CAMEL_CASE"


def snip_func(name):
    insert_snippet(
        f"""{name}($1) {{
            \t$0
        }}"""
    )
