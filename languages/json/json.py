from talon import Context

ctx = Context()

ctx.matches = r"""
code.language: json
code.language: jsonl
"""

ctx.lists["user.code_insert"] = {
    "true": "true",
    "false": "false",
    "null": "null",
}
