from talon import Module, Context

ctx = Context()
mod = Module()

mod.apps.edge = """
os: windows
and app.name: Microsoft Edge
os: windows
and app.exe: msedge.exe
"""

ctx.matches = """
app: edge
"""

ctx.tags = ["browser"]
