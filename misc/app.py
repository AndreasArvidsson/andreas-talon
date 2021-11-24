from talon import Context, Module, actions


mod = Module()
ctx = Context()


@ctx.action_class("app")
class AppActionsWin:
    def window_open():
        actions.key("ctrl-n")

    def window_close():
        actions.key("alt-f4")


@mod.action_class
class Actions:
    def stop_app():
        """Stop current app actions"""
        if actions.user.mouse_stop():
            return
        if actions.user.scroll_stop():
            return
        actions.key("escape:3")

    def mute_microphone():
        """Mute microphone"""

    def pick_item(index: int):
        """Pick list item by index"""
        for _ in range(index):
            actions.edit.down()
        actions.key("enter")
