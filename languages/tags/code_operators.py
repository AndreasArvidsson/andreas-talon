from talon import Module
from dataclasses import dataclass, fields

mod = Module()
mod.tag("code_operators", "Enable code operators")
mod.list("code_operator", "List of code operators")

Operator = str | None


@dataclass
class CodeOperators(dict):
    # ----- Assignment operator -----
    op_assign: Operator = None

    # ----- Math operators -----
    op_sub: Operator = None
    op_sub_assign: Operator = None
    op_add: Operator = None
    op_add_assign: Operator = None
    op_mult: Operator = None
    op_mult_assign: Operator = None
    op_div: Operator = None
    op_div_assign: Operator = None
    op_mod: Operator = None
    op_mod_assign: Operator = None
    op_pow: Operator = None

    # ----- Comparison operators -----
    is_equal: Operator = None
    is_not_equal: Operator = None
    is_less: Operator = None
    is_greater: Operator = None
    is_less_equal: Operator = None
    is_greater_equal: Operator = None
    is_not: Operator = None
    is_null: Operator = None
    is_not_null: Operator = None
    is_in: Operator = None

    # ----- Logical operators -----
    op_in: Operator = None
    op_and: Operator = None
    op_or: Operator = None

    def __post_init__(self):
        for field in fields(self):
            key = field.name.replace("_", " ").strip()
            value = getattr(self, field.name)
            if value is not None:
                self[key] = value
