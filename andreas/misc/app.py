from talon import Context, actions
key = actions.key

ctx = Context()

@ctx.action_class("app")
class AppActionsWin:
    def window_open():      key("ctrl-n")
    def window_close():     key("alt-f4")
