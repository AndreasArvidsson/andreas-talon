from talon import Context, Module, actions


mod = Module()
ctx = Context()


@ctx.action_class("app")
class AppActions:
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
        actions.key("escape")

    def mute_microphone():
        """Mute microphone"""

    def pick_item(index: int):
        """Pick list item by index"""
        for _ in range(index):
            actions.edit.down()
        actions.key("enter")

    def insert_arrow():
        """Insert arrow symbol"""
        actions.insert(" => ")


# ----- WINDOWS -----

ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""


@ctx_win.action_class("app")
class AppActionsWin:
    def window_hide():
        actions.key("alt-space")
        actions.sleep("50ms")
        actions.key("n")


# ----- LINUX -----

ctx_linux = Context()
ctx_linux.matches = r"""
os: linux
"""


@ctx_linux.action_class("app")
class AppActionsLinux:
    def window_hide():
        actions.key("alt-space")
        actions.sleep("200ms")
        actions.key("space")
