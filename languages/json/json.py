from talon import Context

ctx = Context()

ctx.matches = r"""
code.language: json
code.language: jsonl
"""

ctx.lists["self.code_insert"] = {
    "true": "true",
    "false": "false",
}
