from talon import Module

mod = Module()

mod.tag("voip")


@mod.action_class
class Actions:
    def mute_microphone():
        """Mute microphone"""
