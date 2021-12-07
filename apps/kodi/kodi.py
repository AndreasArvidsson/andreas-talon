from talon import Context, actions

ctx = Context()


@ctx.action_class("user")
class UserActions:
    def go_back():
        actions.key("backspace")
