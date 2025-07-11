from talon import Module, actions, settings
from typing import Optional, Union

mod = Module()

mod.tag("code_generic_language")

mod.list("code_class_modifier", "Class modifiers")
mod.list("code_function_modifier", "Function modifiers")
mod.list("code_variable_modifier", "Variable modifiers")
mod.list("code_symbol", "Known symbols in the code workspace")

mod.setting("code_class_formatter", type=str, desc="Class name formatter")
mod.setting("code_function_formatter", type=str, desc="Function name formatter")
mod.setting("code_variable_formatter", type=str, desc="Variable name formatter")


@mod.action_class
class Actions:
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
        name: str,
        modifiers: Union[list[str], str],
        assign: bool,
        data_type: str = None,
    ):
        """Variable statement wrapper"""
        format = actions.user.code_get_variable_format()
        name = actions.user.format_text(name, format)
        actions.user.code_variable(name, modifiers or [], assign, data_type)

    def code_variable(
        name: str,
        modifiers: list[str],
        assign: bool,
        data_type: str = None,
    ):
        """Variable statement"""

    # ----- New instance  -----
    def code_new_instance(name: str):
        """Create new instance of <name>"""
        actions.user.insert_snippet_by_name("newInstance", {"name": name})

    # ----- Formatting getters -----
    def code_get_class_format() -> str:
        """Get class format"""
        return settings.get("user.code_class_formatter")  # type: ignore

    def code_get_function_format() -> str:
        """Get function format"""
        return settings.get("user.code_function_formatter")  # type: ignore

    def code_get_variable_format() -> str:
        """Get variable format"""
        return settings.get("user.code_variable_formatter")  # type: ignore

    # ----- Text getters -----
    def code_get_class_name() -> Optional[str]:
        """Get class name"""

    def code_get_open_tag_name() -> Optional[str]:
        """Get class name"""


def parse_function_name(name: str) -> str:
    format = actions.user.code_get_function_format()
    name = actions.user.format_text(name, format)
    return name
