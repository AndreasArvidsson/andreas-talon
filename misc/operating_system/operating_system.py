from talon import Context, Module, actions
import os


mod = Module()
mod.list("launch_command", desc="List of applications to launch")

ctx = Context()
ctx.lists["self.launch_command"] = {}


@mod.action_class
class Actions:
    def exec(command: str):
        """Run command"""
        os.system(command)

    def shut_down_os():
        """Shut down operating system"""


# ----- Windows -----


ctx_win = Context()

ctx_win.matches = r"""
os: windows
"""

ctx_win.lists["self.launch_command"] = {
    "control panel": "control",
    "sound settings": "control mmsys.cpl sounds",
    "settings": "ms-settings:",
    "paint": "mspaint",
    "notepad": "notepad",
    "explorer": "explorer",
    "code": "code",
}


@ctx_win.action_class("user")
class UserActionsWin:
    def exec(command: str):
        actions.key("super-r")
        actions.sleep("30ms")
        actions.insert(command)
        actions.key("enter")

    def shut_down_os():
        actions.key("super-x u")
