from talon import Context, Module, actions
from talon.grammar import Phrase
from typing import Union

mod = Module()

mod.mode("swedish")

ctx_swedish = Context()

ctx_swedish.matches = r"""
mode: user.swedish
"""

ctx_swedish.settings = {
    "speech.engine": "webspeech",
    "speech.language": "sv_SE"
}


@mod.action_class
class Actions:
    def command_mode(phrase: Union[Phrase, str] = None):
        """Enter command mode and re-evaluate phrase"""
        actions.mode.disable("user.swedish")
        actions.mode.disable("dictation")
        actions.mode.enable("command")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def dictation_mode(phrase: Union[Phrase, str] = None):
        """Enter dictation mode and re-evaluate phrase"""
        actions.mode.disable("command")
        actions.mode.enable("dictation")
        if phrase:
            actions.user.rephrase(phrase, run_async=True)

    def swedish_mode(phrase: Union[Phrase, str] = None):
        """Enter swedish dictation mode and re-evaluate phrase"""
        actions.mode.enable("user.swedish")
        actions.user.dictation_mode(phrase)
