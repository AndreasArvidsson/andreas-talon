from talon import Module, Context
from .javascript import javascript_inserts

mod = Module()

ctx = Context()
ctx.matches = r"""
tag: user.typescript
"""

ctx.lists["self.code_data_type"] = {
    "bool": "boolean",
    "number": "number",
    "string": "string",
    "any": "any",
}

ctx.lists["self.code_insert"] = {
    **javascript_inserts,
    **{
        "public": "public ",
        "private": "private ",
        "protected": "protected ",
    },
}
