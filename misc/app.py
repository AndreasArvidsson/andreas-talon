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

    def mute():
        """Mute conversation"""

    def go_back():
        """Navigate back"""

    def go_forward():
        """Navigate forward"""
