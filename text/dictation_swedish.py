from talon import Module, Context

mod = Module()
ctx = Context()
ctx.matches = r"""
mode: dictation
language: sv_SE
"""


@ctx.action_class("user")
class UserActions:
    def lower_swedish_words(words: list[str]):
        return [w.lower() for w in words]


@mod.action_class
class Actions:
    def lower_swedish_words(words: list[str]):
        """Lower case all words if they are Swedish. Web speech makes annoying capitalizations."""
        return words
