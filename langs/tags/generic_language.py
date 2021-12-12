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
mod.list("code_snippet", desc="Names of miscellaneous text snippets")


@mod.capture(rule="{user.code_function}")
def code_functions(m) -> str:
    """Returns a function name"""
    return m.code_function


@mod.action_class
class tab_actions:
    # ----- Selection statements -----
    def code_if():
        """If statement"""

    def code_elif():
        """Else if statement"""

    def code_else():
        """Else statement"""

    def code_switch():
        """Switch statement"""

    def code_case():
        """case statement"""

    def code_default():
        """Switch default statement"""

    # ----- Iteration statements -----
    def code_for():
        """For loop statement"""

    def code_while():
        """while statement"""

    def code_do_while():
        """Do while loop statements"""

    def code_foreach():
        """Code foreach"""

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

    def code_print(text: str = None):
        """Print statement"""

    def code_format_string():
        """Format string statement"""

    # ----- Class statement -----
    def code_class_wrapper(name: str, modifiers: Union[list[str], str]):
        """Class declaration wrapper"""
        format = actions.user.code_get_class_format()
        name = actions.user.format_text(name, format)
        actions.user.history_add_phrase(name)
        actions.user.code_class(name, modifiers or [])

    def code_class(name: str, modifiers: list[str]):
        """Class declaration"""

    # ----- Constructor statement -----
    def code_constructor_wrapper(modifiers: Union[list[str], str]):
        """Constructor declaration wrapper"""
        actions.user.code_constructor(modifiers or [])

    def code_constructor(modifiers: list[str]):
        """Constructor declaration"""

    # ----- Function statement -----
    def code_function_wrapper(name: str, modifiers: Union[list[str], str]):
        """Function declaration wrapper"""
        name = parse_function_name(name)
        actions.user.code_function(name, modifiers or [])

    def code_method_wrapper(name: str, modifiers: Union[list[str], str]):
        """Method declaration wrapper"""
        name = parse_function_name(name)
        actions.user.code_method(name, modifiers or [])

    def code_function(name: str, modifiers: list[str]):
        """Function declaration"""

    def code_method(name: str, modifiers: list[str]):
        """Method declaration"""
        actions.user.code_function(name, modifiers)

    def code_function_main():
        """Main function declaration"""

    # ----- Variable statement -----
    def code_variable_wrapper(
        name: str, modifiers: Union[list[str], str], assign: int, data_type: str = None
    ):
        """Variable statement wrapper"""
        format = actions.user.code_get_variable_format()
        name = actions.user.format_text(name, format)
        actions.user.history_add_phrase(name)
        actions.user.code_variable(name, modifiers or [], bool(assign), data_type)

    def code_variable(
        name: str, modifiers: list[str], assign: bool, data_type: str = None
    ):
        """Variable statement"""

    # ----- Function call -----
    def code_call_function(name: str):
        """Function call"""

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
    actions.user.history_add_phrase(name)
    return name
