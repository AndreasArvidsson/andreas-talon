from talon import Module, Context, actions


mod = Module()
mod.tag("tabs")

ctx = Context()
ctx.matches = r"""
tag: user.tabs
"""


@ctx.action_class("app")
class AppActions:
    def tab_previous():
        actions.key("ctrl-shift-tab")

    def tab_next():
        actions.key("ctrl-tab")

    def tab_open():
        actions.key("ctrl-t")

    def tab_close():
        actions.key("ctrl-w")

    def tab_reopen():
        actions.key("ctrl-shift-t")


@mod.action_class
class TabActions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""
        actions.key(f"ctrl-{number}")

    def tab_jump_from_back(number: int):
        """Jumps to the specified tab counted from the back"""
        actions.user.tab_final()
        for _ in range(number - 1):
            actions.app.tab_previous()

    def tab_final():
        """Jumps to the final tab"""
        actions.user.tab_jump(1)
        actions.app.tab_previous()

    def tab_move_left():
        """Move tab to the left"""
        actions.key("ctrl-shift-pageup")

    def tab_move_right():
        """Move tab to the right"""
        actions.key("ctrl-shift-pagedown")

    def tab_duplicate():
        """Duplicate tab"""

    def tab_back():
        """Jump to last used tab"""
