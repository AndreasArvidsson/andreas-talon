from talon import Module, Context, actions

mod = Module()

mod.mode("game", "Used to play games")
mod.mode("game_voip_muted", "Signals that game voice chat is muted")
mod.tag("game_commands", "Signals that voice commands are enabled in the game")

ctx = Context()
ctx.matches = r"""
mode: user.game
"""

ctx.settings = {
    "user.foot_switch_timeout": False,
    "speech.timeout": 0.05,
}

ctx_commands = Context()
ctx_commands.matches = r"""
mode: user.game
and mode: user.game_voip_muted
and not mode: sleep
"""

ctx_commands.tags = ["user.game_commands"]


@mod.action_class
class Actions:
    def game_mode_enable():
        """Enable game mode"""
        actions.mode.disable("command")
        actions.mode.enable("user.game_voip_muted")
        actions.mode.enable("user.game")

    def game_mode_disable():
        """Disable game mode"""
        actions.mode.disable("user.game")
        actions.mode.disable("user.game_voip_muted")
        actions.mode.enable("command")

    def game_toggle_mute():
        """Toggle voice chat for game"""
        actions.user.abort_current_phrase()
        actions.mode.toggle("user.game_voip_muted")
        actions.user.mute_discord()
