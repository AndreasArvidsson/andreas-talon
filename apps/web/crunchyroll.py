from talon import Context, Module

ctx = Context()
mod = Module()

mod.apps.crunchyroll = r"""
tag: browser
browser.host: www.crunchyroll.com
browser.path: /^/watch/.*/
"""

ctx.matches = r"""
app: crunchyroll
"""

ctx.settings = {
    "user.mode_indicator_show": False,
}
