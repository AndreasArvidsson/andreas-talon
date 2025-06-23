from talon import Context, Module, actions, app

mod = Module()
ctx = Context()

mod.mode("demo", "Used for demos")


ctx_dictation = Context()
ctx_dictation.matches = r"""
mode: dictation
"""


@ctx.action_class("user")
class UserActions:
    def command_dictation_mode_toggle():
        actions.user.dictation_mode()


@ctx_dictation.action_class("user")
class DictationUserActions:
    def command_dictation_mode_toggle():
        actions.user.command_mode()


@mod.action_class
class Actions:
    def command_mode():
        """Enter command mode"""
        ctx.settings = {}
        actions.mode.disable("dictation")
        actions.mode.disable("user.demo")
        actions.mode.enable("command")

    def dictation_mode():
        """Enter dictation mode"""
        actions.user.dictation_format_reset()
        actions.mode.disable("command")
        actions.mode.disable("user.demo")
        actions.mode.enable("dictation")

    def command_dictation_mode_toggle():
        """Toggle between command and dictation mode"""

    def swedish_dictation_mode():
        """Enter swedish dictation mode"""
        ctx.settings = {
            "speech.language": "sv_SE",
        }
        actions.user.dictation_mode()

    def mixed_mode():
        """Enter mixed mode"""
        actions.user.dictation_format_reset()
        actions.mode.enable("dictation")

    def demo_mode():
        """Enter demo mode"""
        actions.mode.disable("command")
        actions.mode.disable("dictation")
        actions.mode.enable("user.demo")

    def talon_sleep():
        """Put Talon to sleep"""
        actions.speech.disable()
        actions.user.mouse_sleep()
        actions.user.notify("Talon sleeping")

    def talon_wake():
        """Wake Talon from sleep"""
        actions.user.abort_current_phrase()
        actions.speech.enable()
        actions.user.mouse_wake()
        actions.user.notify("Talon awake")


def on_launch():
    if not actions.user.talon_was_restarted():
        actions.user.talon_sleep()


app.register("launch", on_launch)
