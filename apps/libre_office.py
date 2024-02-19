from talon import Context, Module

ctx = Context()
mod = Module()

mod.apps.libre_office = r"""
os: windows
and app.exe: soffice.bin
os: linux
and app.name: libreoffice-calc
"""

ctx.matches = r"""
app: libre_office
"""

ctx.tags = ["user.find"]
