from talon import Context, Module, actions
from subprocess import call
import os

key = actions.key

mod = Module()
mod.list("playback_device", desc="Playback devices")
mod.list("microhpone_device", desc="Microphone devices")
mod.list("playback_microphone_pair", desc="Playback / microphone device pair")


@mod.action_class
class Actions:
    def volume_up():
        """Volume increase"""
        key("volup")

    def volume_down():
        """Volume decrease"""
        key("voldown")

    def change_sound_device(name: str):
        """Change sound device."""

    def change_sound_device_pair(name: str):
        """Change sound device pair."""


# ----- WINDOWS -----

ctx_win = Context()

ctx_win.matches = r"""
os: windows
"""

ctx_win.lists["self.playback_device"] = [
    "Headphones",
    "Speakers",
]

ctx_win.lists["self.microhpone_device"] = {
    "Headphones": "Headphones_mic",
    "AKG": "Focusrite",
}

playback_microphone_pair = {
    "Headphones": ["Headphones", "Headphones_mic"],
    "AKG": ["Speakers", "Focusrite"],
}
ctx_win.lists["self.playback_microphone_pair"] = playback_microphone_pair.keys()


@ctx_win.action_class("user")
class UserActionsWin:
    def change_sound_device(name: str):
        change_sound_device_win(name, 1)
        change_sound_device_win(name, 2)

    def change_sound_device_pair(name: str):
        pair = playback_microphone_pair[name]
        actions.user.notify(f"Using {pair[0]} / {pair[1]}")
        actions.user.change_sound_device(pair[0])
        actions.user.change_sound_device(pair[1])


def change_sound_device_win(name: str, role: int):
    """Roles: 0: Console, 1: Multimedia, 2: Communications"""
    program_files = os.environ["ProgramFiles"]
    call(
        [f"{program_files}/nircmd/nircmd.exe", "setdefaultsounddevice", name, f"{role}"]
    )
