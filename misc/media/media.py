from talon import Context, Module, actions
from subprocess import call
import os

key = actions.key

mod = Module()
mod.list("playback_device", desc="Playback devices")
mod.list("microhpone_device", desc="Microphone devices")


@mod.action_class
class Actions:
    def volume_up():
        """Volume increase"""
        key("volup")

    def volume_down():
        """Volume decrease"""
        key("voldown")

    def change_sound_device(name: str, role: str):
        """Change sound device. Roles: 0: Console, 1: Multimedia, 2: Communications"""


# ----- WINDOWS -----

ctx_win = Context()

ctx_win.matches = r"""
os: windows
"""

ctx_win.lists["self.playback_device"] = ["Headphones", "Speakers"]

ctx_win.lists["self.microhpone_device"] = {
    "Headphones": "Realtek",
    "Microphone": "Focusrite",
}

@ctx_win.action_class("user")
class UserActionsWin:
    def change_sound_device(name: str, role: str):
        program_files = os.environ["ProgramFiles"]
        call(
            [f"{program_files}/nircmd/nircmd.exe", "setdefaultsounddevice", name, role]
        )
