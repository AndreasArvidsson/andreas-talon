from talon import Module, Context

ctx = Context()
mod = Module()

mod.apps.edge = r"""
os: windows
and app.exe: msedge.exe
"""

ctx.matches = r"""
app: edge
"""

ctx.tags = ["browser"]
