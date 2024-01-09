from talon import Module, Context

mod = Module()

mod.apps.netflix = """
os: windows
and app.exe: ApplicationFrameHost.exe
and win.title: Netflix

os: windows
and tag: browser
and browser.host: www.netflix.com
"""

ctx = Context()

ctx.matches = r"""
app: netflix
"""

ctx.settings = {
    "user.mode_indicator_show": False,
}
