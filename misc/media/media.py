from talon import Context, Module, actions, app
from subprocess import call
import os
key = actions.key

mod = Module()
mod.list("playback_devices", desc="Playback devices")

@mod.action_class
class Actions:
    def volume_up():
        """Volume increase"""
        key("volup")
    def volume_down():
        """Volume decrease"""
        key("voldown")
    def change_playback_device(name: str):
        """Change playback device"""


# ----- WINDOWS -----

ctx_win = Context()

ctx_win.matches = r"""
os: windows
"""

ctx_win.lists["self.playback_devices"] = [
    "Headphones",
    "Speakers"
]

@ctx_win.action_class("user")
class UserActionsWin:
    def change_playback_device(name: str):
        app.notify(f"Playback device:\n{name}")
        program_files = os.environ["ProgramFiles"]
        call([
             f"{program_files}/nircmd/nircmd.exe",
             "setdefaultsounddevice",
             name
             ])
