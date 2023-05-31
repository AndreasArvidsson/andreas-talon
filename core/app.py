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
        if actions.user.mouse_scroll_stop():
            return
        if actions.user.scroll_stop():
            return
        actions.key("escape")

    def pick_item(number: int):
        """Pick list item number <number>"""
        for _ in range(number - 1):
            actions.edit.down()
        actions.key("enter")


# ----- WINDOWS -----

ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""


@ctx_win.action_class("app")
class AppActionsWin:
    def window_hide():
        actions.key("alt-space")
        actions.sleep("100ms")
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
