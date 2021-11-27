from talon import Module, Context


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
