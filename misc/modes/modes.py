from talon import Context, Module, actions, app
from talon.grammar import Phrase
from typing import Union

mod = Module()
ctx = Context()


@mod.action_class
class Actions:
    def command_mode(phrase: Union[Phrase, str] = None):
        """Enter command mode and re-evaluate phrase"""
        ctx.tags = []
        actions.mode.disable("dictation")
        actions.mode.enable("command")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def dictation_mode(phrase: Union[Phrase, str] = None):
        """Enter dictation mode and re-evaluate phrase"""
        actions.user.dictation_format_reset()
        actions.mode.disable("command")
        actions.mode.enable("dictation")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def swedish_mode(phrase: Union[Phrase, str] = None):
        """Enter swedish dictation mode and re-evaluate phrase"""
        ctx.tags = ["user.swedish"]
        actions.user.dictation_mode(phrase)

    def mixed_mode(phrase: Union[Phrase, str] = None):
        """Enter mixed mode and re-evaluate phrase"""
        actions.user.dictation_format_reset()
        actions.mode.enable("dictation")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)


def on_ready():
    """Disabled not used modes"""
    actions.mode.disable("face")


app.register("ready", on_ready)
