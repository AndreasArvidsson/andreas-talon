from talon import Context, Module

ctx = Context()
mod = Module()

mod.apps.disneyplus = r"""
tag: browser
browser.host: www.disneyplus.com
"""

ctx.matches = r"""
app: disneyplus
"""

ctx.settings = {
    "user.mode_indicator_show": False,
}
