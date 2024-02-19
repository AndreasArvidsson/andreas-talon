from talon import Module, Context

mod = Module()

mod.apps.netflix = r"""
os: windows
and app.exe: applicationframehost.exe
and win.title: Netflix

tag: browser
and browser.host: www.netflix.com
"""

ctx = Context()

ctx.matches = r"""
app: netflix
"""

ctx.settings = {
    "user.mode_indicator_show": False,
}
