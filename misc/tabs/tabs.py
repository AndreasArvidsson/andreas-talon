from talon import Module, Context, actions
key = actions.key

mod = Module()
mod.tag("tabs")

ctx = Context()
ctx.matches = r"""
tag: user.tabs
"""


@ctx.action_class("app")
class AppActions:
    def tab_previous():     key("ctrl-pageup")
    def tab_next():         key("ctrl-pagedown")
    def tab_open():         key("ctrl-t")
    def tab_close():        key("ctrl-w")
    def tab_reopen():       key("ctrl-shift-t")


@mod.action_class
class TabActions:
    def tab_jump(number: int):
        """Jumps to the specified tab"""
        key(f"ctrl-{number}")

    def tab_final():
        """Jumps to the final tab"""
        key("ctrl-0")

    def tab_move_left():
        """Move tab to the left"""
        key("ctrl-shift-pageup")

    def tab_move_right():
        """Move tab to the right"""
        key("ctrl-shift-pagedown")

    def tab_duplicate():
        """Duplicate tab"""

    def tab_mute():
        """Mute current tab"""
