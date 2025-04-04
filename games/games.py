from talon import Module, Context, ctrl, actions

mod = Module()

mod.mode("game", "Used to play games")
mod.tag("game_voip_muted", "Signals that game voice chat is muted")

ctx = Context()
ctx.matches = r"""
mode: user.game
"""

ctx.settings = {
    "speech.timeout": 0.05,
}


@ctx.action_class("main")
class MainActions:
    def mouse_click(button: int = 0):
        ctrl.mouse_click(button=button, hold=16000)


@ctx.action_class("speech")
class SpeechActions:
    def disable():
        actions.mode.save()
        actions.mode.disable("user.game")
        actions.mode.enable("sleep")


@mod.action_class
class Actions:
    def game_mode_enable():
        """Enable game mode"""
        actions.mode.disable("command")
        actions.mode.enable("user.game")
        update_tag(
            voip_muted(),
        )

    def game_mode_disable():
        """Disable game mode"""
        actions.mode.disable("user.game")
        actions.mode.enable("command")
        actions.user.mouse_release_held_buttons()

    def game_toggle_mute():
        """Toggle voice chat for game"""
        actions.user.abort_current_phrase()
        update_tag(
            actions.user.discord_toggle_mute(),
        )


def update_tag(voip_muted: bool):
    if voip_muted:
        ctx.tags = ["user.game_voip_muted"]
    else:
        ctx.tags = []


def voip_muted() -> bool:
    try:
        return actions.user.discord_get_mute_status()
    except Exception:
        return True
