from talon import Module, actions
from typing import Optional, Union

mod = Module()

mod.tag("code_keywords", "Enable code keyword commands")
mod.tag("code_operators", "Enable code operator commands")
mod.tag("code_variables", "Enable code variable commands")
mod.tag("code_function_calls", "Enable code function call commands")
mod.tag("code_constructors", "Enable code constructor commands")
mod.tag("code_types", "Enable code type commands")
mod.tag("code_comments", "Enable code comment commands")

mod.list("code_variable_modifier", "Variable modifiers")
mod.list("code_function", "Names of functions to call")
mod.list("code_keyword", "Names of miscellaneous text insertions")
mod.list("code_operator", "List of code operators")
mod.list("code_data_type", "Names of data types")
mod.list("code_collection_type", "Names of collection data types")

mod.setting("code_class_formatter", type=str, desc="Class name formatter")
mod.setting("code_function_formatter", type=str, desc="Function name formatter")
mod.setting("code_variable_formatter", type=str, desc="Variable name formatter")


@mod.capture(rule="{user.code_keyword}+")
def code_keywords(m) -> str:
    """Returns multiple code inserts join together"""
    return " ".join(m.code_keyword_list).replace("  ", " ")


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
        formatter = actions.settings.get("user.code_variable_formatter")
        name = actions.user.format_text(name, formatter)
        actions.user.code_variable(assign, modifiers or [], data_type, name)

    @staticmethod
    def code_variable(assign: bool, modifiers: list[str], data_type: str, name: str):
        """Variable statement"""

    # ----- Function call statement -----
    @staticmethod
    def code_call_function(name: str):
        """Call function <name>"""
        actions.user.insert_snippet_by_name("functionCall", {"1": name})

    @staticmethod
    def code_call_function_with_phrase(phrase: str):
        """Call function <name>"""
        formatter: str = actions.settings.get("user.code_function_formatter")
        name = actions.user.format_text(phrase, formatter)
        actions.user.code_call_function(name)

    # ----- New instance statement -----
    @staticmethod
    def code_new_instance(name: str):
        """Create new instance of <name>"""
        actions.user.insert_snippet_by_name("newInstance", {"1": name})

    @staticmethod
    def code_new_instance_with_phrase(phrase: str):
        """Create new instance of <phrase>"""
        formatter: str = actions.settings.get("user.code_class_formatter")
        name = actions.user.format_text(phrase, formatter)
        actions.user.code_new_instance(name)

    # ----- Comment statements -----
    @staticmethod
    def insert_todo_comment(message: Optional[str] = None):
        """Inserts a TODO comment"""
        message = actions.user.format_text(message or "", "SENTENCE")
        actions.user.insert_snippet_by_name("commentLine", {"1": f"TODO: {message}"})

    @staticmethod
    def insert_fixme_comment(message: Optional[str] = None):
        """Inserts a FIXME comment"""
        message = actions.user.format_text(message or "", "SENTENCE")
        actions.user.insert_snippet_by_name("commentLine", {"1": f"FIXME: {message}"})

    # ----- Text getters -----
    def code_get_class_name() -> Optional[str]:
        """Get class name"""

    def code_get_open_tag_name() -> Optional[str]:
        """Get class name"""
