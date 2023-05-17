from talon import Module, Context

mod = Module()

mod.apps.netflix = """
os: windows
and app.exe: ApplicationFrameHost.exe
and win.title: Netflix
"""

ctx = Context()

ctx.matches = r"""
app: netflix
"""

ctx.settings = {
    "user.mode_indicator_show": False,
}
