from contextlib import suppress

from talon import Module, actions

mod = Module()

mod.list("code_data_type", "Names of data types")
mod.list("code_collection_type", "Names of collection data types")


# "int or list of str"
@mod.capture(rule="<user.code_data_single_type> (or <user.code_data_single_type>)*")
def code_data_type(m) -> str:
    types = m.code_data_single_type_list
    return actions.user.code_format_or_type(types) if len(types) > 1 else types[0]


# "int or string" | "list of int" | "int array"
@mod.capture(
    rule="<user.code_simple_union_type> | <user.code_collection_type> | <user.code_array_type>"
)
def code_data_single_type(m) -> str:
    return m[0]


# "list of int" | "record of string and number"
@mod.capture(
    rule="{user.code_collection_type} of <user.code_simple_union_type> (and <user.code_simple_union_type>)*"
)
def code_collection_type(m) -> str:
    items = []
    with suppress(AttributeError):
        items = m.code_simple_union_type_list
    return actions.user.code_format_collection_type(m.code_collection_type, items)


# "int array" | "int list"
@mod.capture(rule="<user.code_simple_union_type> (array | list)")
def code_array_type(m) -> str:
    return actions.user.code_format_array_type(m.code_simple_union_type)


# "int or list or my class"
@mod.capture(rule="<user.code_simple_data_type> (or <user.code_simple_data_type>)*")
def code_simple_union_type(m) -> str:
    types = m.code_simple_data_type_list
    return actions.user.code_format_or_type(types) if len(types) > 1 else types[0]


# "int" | "list" | "my class"
@mod.capture(rule="{user.code_data_type} | {user.code_collection_type} | <user.prose>")
def code_simple_data_type(m) -> str:
    with suppress(AttributeError):
        return m.code_data_type
    with suppress(AttributeError):
        return m.code_collection_type
    format = actions.user.code_get_class_format()
    return actions.user.format_text(m.prose, format)


@mod.action_class
class Actions:
    def code_insert_type_annotation(type: str):
        """Insert type annotation <type>"""

    def code_insert_return_type(type: str):
        """Insert return type <type>"""

    def code_format_collection_type(collection_type: str, item_types: list[str]) -> str:
        """Format collection type <collection_type> with types <data_types>"""

    def code_format_array_type(item_type: str) -> str:
        """Format array with types <data_type>"""

    def code_format_or_type(item_types: list[str]) -> str:
        """Format or type with types <data_types>"""
