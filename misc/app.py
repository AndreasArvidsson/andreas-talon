from talon import Context, Module, actions
key = actions.key

ctx = Context()
mod = Module()


@ctx.action_class("app")
class AppActionsWin:
    def window_open():       key("ctrl-n")
    def window_close():      key("alt-f4")


@mod.action_class
class Actions:
    def stop_app():
        """Stop current app actions"""
        if not actions.user.mouse_stop():
            actions.key("escape:3")
