from talon import Module, Context

ctx = Context()
mod = Module()

mod.apps.chrome = """
os: windows
and app.name: Google Chrome
os: windows
and app.exe: chrome.exe
"""

ctx.matches = """
app: chrome
"""

ctx.tags = ["browser"]
