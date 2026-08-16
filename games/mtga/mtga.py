from talon import Context, Module, ctrl

mod = Module()

mod.apps.mtga = r"""
os: windows
and app.exe: mtga.exe
"""

ctx = Context()

ctx.matches = r"""
app: mtga
"""


@ctx.action_class("main")
class MainActions:
    @staticmethod
    def mouse_click(button: int = 0):
        ctrl.mouse_click(button=button, hold=16000)
