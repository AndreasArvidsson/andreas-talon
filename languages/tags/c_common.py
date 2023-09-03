from talon import Module, Context

mod = Module()
ctx = Context()

mod.tag("c_common")

ctx.matches = r"""
tag: user.c_common
"""


@ctx.action_class("user")
class UserActions:
    # Formatting getters
    def code_get_class_format() -> str:
        return "PASCAL_CASE"

    def code_get_function_format() -> str:
        return "CAMEL_CASE"

    def code_get_variable_format() -> str:
        return "CAMEL_CASE"
