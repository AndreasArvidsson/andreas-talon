from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def recording_start():
        """Start recording"""
        send_key("alt-f9")

    def recording_stop():
        """Stop recording"""
        send_key("alt-f10")


def send_key(key: str):
    actions.user.send_key(
        key,
        actions.user.get_app("OBS Studio"),
    )
