from talon import Module, Context
from .javascript import javascript_statements

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

ctx.lists["self.code_statement"] = {
    **javascript_statements,
    **{
        "public": "public ",
        "private": "private ",
        "protected": "protected ",
    },
}
