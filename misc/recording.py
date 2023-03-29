from talon import Module, actions

mod = Module()


@mod.action_class
class Actions:
    def recording_start():
        """Start recording"""
        actions.key("alt-f9:down")
        actions.sleep("100ms")
        actions.key("alt-f9:up")

    def recording_stop():
        """Stop recording"""
        actions.key("alt-f10:down")
        actions.sleep("100ms")
        actions.key("alt-f10:up")


def send_key(key: str):
    actions.user.send_key(
        key,
        actions.user.get_app("OBS Studio"),
    )
