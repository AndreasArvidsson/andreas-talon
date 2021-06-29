from talon import Module, actions, app
from talon.grammar import Phrase

mod = Module()

@mod.action_class
class Actions:
    def command_mode(phrase: Phrase = None):
        """Enter command mode and re-evaluate phrase"""
        actions.mode.disable("dictation")
        actions.mode.enable("command")
        app.notify("Command mode")
        if phrase:
            actions.user.rephrase(phrase)

    def dictation_mode(phrase: Phrase = None):
        """Enter dictation mode and re-evaluate phrase"""
        actions.mode.disable("command")
        actions.mode.enable("dictation")
        app.notify("Dictation mode")
        if phrase:
            actions.user.rephrase(phrase)
