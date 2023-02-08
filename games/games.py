from talon import Module, Context

mod = Module()
ctx = Context()

mod.mode("game", "Used to play games")
mod.tag("game_speech", "Signals that speech commands are enabled in the game")

ctx.matches = r"""
mode: user.game
and mode: user.discord_muted
and not mode: sleep
"""

ctx.tags = ["user.game_speech"]
