from talon import Context, Module, actions, app
from subprocess import call

mod = Module()
mod.list("playback_device", "Playback devices")
mod.list("microhpone_device", "Microphone devices")
mod.list("sound_device_pair", "Sound devices (microphone and playback)")


@mod.action_class
class Actions:
    def volume_up():
        """Volume increase"""
        actions.key("volup")

    def volume_down():
        """Volume decrease"""
        actions.key("voldown")

    def change_sound_device_pair(name: str):
        """Change sound device pair <name>"""
        microphone, playback = name.split(",")
        actions.user.change_sound_device(microphone)
        actions.user.change_sound_device(playback)

    def change_sound_device(name: str):
        """Change sound device <name>"""

    def sound_microphone_enabled() -> bool:
        """Returns true if the microphone is NOT set to 'None'"""
        return actions.sound.active_microphone() != "None"

    def sound_microphone_enable(enable: bool):
        """Enables or disables the microphone"""
        if enable:
            actions.sound.set_microphone("System Default")
            actions.user.notify("Activating microphone")
        else:
            actions.sound.set_microphone("None")
            actions.user.notify("Deactivating microphone")
        actions.user.sound_microphone_enable_event()

    def sound_microphone_toggle():
        """Toggle the microphone"""
        actions.user.sound_microphone_enable(
            not actions.user.sound_microphone_enabled()
        )

    def sound_microphone_enable_event():
        """Event that triggers when the microphone is enabled or disabled"""
        actions.skip()


# ----- WINDOWS -----

ctx_win = Context()

ctx_win.matches = r"""
os: windows
"""

ctx_win.lists["user.playback_device"] = {
    "speakers": "Speakers",
    "headphones": "Koss headphones",
    "koss": "Koss headphones",
}

ctx_win.lists["user.microhpone_device"] = {
    "dpa": "DPA",
    "blue yeti": "Blue Yeti",
    "headphones": "Koss microphone",
    "koss": "Koss microphone",
    # "internal": "Internal_mic",
    # "camera": "Webcam",
}


ctx_win.lists["user.sound_device_pair"] = {
    "dpa": "DPA,Speakers",
    "blue yeti": "Blue Yeti,Speakers",
    "koss": "Koss microphone,Koss headphones",
}


@ctx_win.action_class("user")
class UserActionsWin:
    def change_sound_device(name: str):
        change_sound_device_win(name, 1)
        change_sound_device_win(name, 2)


def change_sound_device_win(name: str, role: int):
    """Roles: 0: Console, 1: Multimedia, 2: Communications"""
    call(["nircmd.exe", "setdefaultsounddevice", name, str(role)])


def on_launch():
    actions.sound.set_microphone("System Default")


app.register("launch", on_launch)
