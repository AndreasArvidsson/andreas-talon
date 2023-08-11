from typing import Union
from talon import Module, actions

mod = Module()
mod.tag("generic_language")

mod.list("code_class_modifier", desc="Class modifiers")
mod.list("code_function_modifier", desc="Function modifiers")
mod.list("code_variable_modifier", desc="Variable modifiers")
mod.list("code_data_type", desc="Names of data types")
mod.list("code_function", desc="Names of functions")
mod.list("code_insert", desc="Names of miscellaneous text insertions")


@mod.capture(rule="{user.code_insert}+")
def code_inserts(m) -> str:
    """Returns multiple code inserts join together"""
    return " ".join(m.code_insert_list).replace("  ", " ")


@mod.action_class
class tab_actions:
    # ----- Miscellaneous statements -----
    def code_true():
        """Boolean true"""

    def code_false():
        """Boolean false"""

    def code_break():
        """break statement"""

    def code_continue():
        """continue statement"""

    def code_return():
        """return statement"""

    def code_link(text: str = ""):
        """Insert link <text>"""

    # ----- Class statement -----
    def code_class_wrapper(name: str, modifiers: Union[list[str], str]):
        """Declare class <name>"""
        format = actions.user.code_get_class_format()
        name = actions.user.format_text(name, format)
        actions.user.code_class(name, modifiers or [])

    def code_class(name: str, modifiers: list[str]):
        """Declare class <name>"""

    # ----- Constructor statement -----
    def code_constructor_wrapper(modifiers: Union[list[str], str]):
        """Constructor declaration wrapper"""
        actions.user.code_constructor(modifiers or [])

    def code_constructor(modifiers: list[str]):
        """Constructor declaration"""
        actions.user.code_function("constructor", [])

    # ----- Function statement -----
    def code_function_wrapper(name: str, modifiers: Union[list[str], str]):
        """Declare function <name>"""
        name = parse_function_name(name)
        actions.user.code_function(name, modifiers or [])

    def code_method_wrapper(name: str, modifiers: Union[list[str], str]):
        """Declare method <name>"""
        name = parse_function_name(name)
        actions.user.code_method(name, modifiers or [])

    def code_function(name: str, modifiers: list[str]):
        """Declare function <name>"""

    def code_method(name: str, modifiers: list[str]):
        """Declare method <name>"""
        actions.user.code_function(name, modifiers)

    def code_function_main():
        """Main function declaration"""
        actions.user.code_function("main", [])

    # ----- Variable statement -----
    def code_variable_wrapper(
        name: str, modifiers: Union[list[str], str], assign: bool, data_type: str = None
    ):
        """Variable statement wrapper"""
        format = actions.user.code_get_variable_format()
        name = actions.user.format_text(name, format)
        actions.user.code_variable(name, modifiers or [], assign, data_type)

    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        """Variable statement"""

    # ----- Function call -----
    def code_call_function(name: str):
        """Call function <name>"""
        actions.user.code_insert_snippet("functionCall", {"name": name})

        # ----- New instance  -----

    def code_new_instance(name: str):
        """Create new instance of <name>"""
        actions.user.code_insert_snippet("newInstance", {"name": name})

    # ----- Insert types -----
    def code_insert_type_annotation(type: str):
        """Insert type annotation <type>"""

    def code_insert_return_type(type: str):
        """Insert return type <type>"""

    # ----- Formatting getters -----
    def code_get_class_format() -> str:
        """Get variable format"""

    def code_get_function_format() -> str:
        """Get function format"""

    def code_get_variable_format() -> str:
        """Get variable format"""


def parse_function_name(name: str) -> str:
    format = actions.user.code_get_function_format()
    name = actions.user.format_text(name, format)
    return name
