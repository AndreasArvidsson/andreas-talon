from talon import Context

# ----- Windows -----

ctx_win = Context()

ctx_win.matches = r"""
os: windows
os: linux
"""


@ctx_win.action_class("app")
class AppActionsWin:
    def window_open():      key("ctrl-n")
    def window_close():     key("alt-f4")
