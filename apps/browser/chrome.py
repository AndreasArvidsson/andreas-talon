from talon import Module, Context, actions

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


@ctx.action_class("browser")
class BrowserActions:
    def open_private_window():
        actions.key("ctrl-shift-n")
