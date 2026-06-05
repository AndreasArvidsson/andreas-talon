from talon import Module, actions
from typing import Optional, Union

mod = Module()

mod.tag("code_generic_language")

mod.list("code_variable_modifier", "Variable modifiers")

mod.setting("code_class_formatter", type=str, desc="Class name formatter")
mod.setting("code_function_formatter", type=str, desc="Function name formatter")
mod.setting("code_variable_formatter", type=str, desc="Variable name formatter")


@mod.action_class
class Actions:
    # ----- Constructor statement -----
    def code_constructor():
        """Constructor declaration"""
        actions.user.insert_snippet_by_name("constructorDeclaration")

    def code_constructor_with_class_name():
        """Constructor declaration with class name"""
        substitutions: dict[str, str] = {}
        name = actions.user.code_get_class_name()
        if name:
            substitutions["1"] = name
        actions.user.insert_snippet_by_name("constructorDeclaration", substitutions)

    # ----- Variable statement -----
    @staticmethod
    def code_variable_wrapper(
        assign: bool,
        modifiers: Union[list[str], str],
        data_type: str,
        name: str,
    ):
        """Variable statement wrapper"""
        format = actions.user.code_get_variable_format()
        name = actions.user.format_text(name, format)
        actions.user.code_variable(assign, modifiers or [], data_type, name)

    @staticmethod
    def code_variable(assign: bool, modifiers: list[str], data_type: str, name: str):
        """Variable statement"""

    # ----- New instance  -----
    @staticmethod
    def code_new_instance(name: str):
        """Create new instance of <name>"""
        actions.user.insert_snippet_by_name("newInstance", {"name": name})

    # ----- Formatting getters -----
    def code_get_class_format() -> str:
        """Get class format"""
        return actions.settings.get("user.code_class_formatter")  # type: ignore

    def code_get_variable_format() -> str:
        """Get variable format"""
        return actions.settings.get("user.code_variable_formatter")  # type: ignore

    # ----- Text getters -----
    def code_get_class_name() -> Optional[str]:
        """Get class name"""

    def code_get_open_tag_name() -> Optional[str]:
        """Get class name"""
