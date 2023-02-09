from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.mode("game", "Used to play games")
mod.mode("game_voip_muted", "Used to signal that game voice chat is muted")
mod.tag("game_commands", "Signals that voice commands are enabled in the game")

ctx.matches = r"""
mode: user.game
and mode: user.game_voip_muted
and not mode: sleep
"""

ctx.tags = ["user.game_commands"]


@mod.action_class
class Actions:
    def game_mode():
        """Enable game mode"""
        actions.mode.disable("command")
        actions.mode.enable("user.game_voip_muted")
        actions.mode.enable("user.game")

    def game_toggle_mute():
        """Toggle voice chat for game"""
        actions.mode.toggle("user.game_voip_muted")
        actions.user.mute_discord()
