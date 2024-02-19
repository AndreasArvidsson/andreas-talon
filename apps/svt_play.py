from talon import Module, Context

mod = Module()

mod.apps.svt_play = r"""
tag: browser
and browser.host: www.svtplay.se
"""

ctx = Context()

ctx.matches = r"""
app: svt_play
"""

ctx.settings = {
    "user.mode_indicator_show": False,
}
