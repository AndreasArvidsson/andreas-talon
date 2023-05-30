from talon import Module, actions


mod = Module()
mod.tag("navigation")


@mod.action_class
class Actions:
    def go_back():
        """Navigate back"""
        actions.key("alt-left")

    def go_forward():
        """Navigate forward"""
        actions.key("alt-right")
