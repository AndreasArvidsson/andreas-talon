from talon import Context, Module

ctx = Context()
mod = Module()

mod.apps.libre_office = """
os: windows
and app.name: LibreOffice
os: windows
and app.exe: soffice.bin
"""

ctx.matches = r"""
app: libre_office
"""

ctx.tags = ["user.find"]

ctx.settings = {
    "user.scroll_step": 10
}
