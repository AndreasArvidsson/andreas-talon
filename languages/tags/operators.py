from talon import Module
from dataclasses import dataclass, fields

mod = Module()
mod.tag("code_operators", "Enable code operators")
mod.list("code_operator", "List of code operators")


@dataclass
class CodeOperators(dict):
    # ----- Assignment operator -----
    op_assign: str = None

    # ----- Math operators -----
    op_sub: str = None
    op_sub_assign: str = None
    op_add: str = None
    op_add_assign: str = None
    op_mult: str = None
    op_mult_assign: str = None
    op_div: str = None
    op_div_assign: str = None
    op_mod: str = None
    op_mod_assign: str = None
    op_pow: str = None

    # ----- Comparison operators -----
    is_equal: str = None
    is_not_equal: str = None
    is_less: str = None
    is_greater: str = None
    is_less_equal: str = None
    is_greater_equal: str = None
    is_not: str = None
    is_null: str = None
    is_not_null: str = None
    is_in: str = None

    # ----- Logical operators -----
    op_and: str = None
    op_or: str = None

    def __post_init__(self):
        for field in fields(self):
            key = field.name.replace("_", " ").strip()
            value = getattr(self, field.name)
            if value is not None:
                self[key] = value
