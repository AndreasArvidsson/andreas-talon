from talon import Module

mod = Module()

@mod.action_class
class Actions:
    def browser_open(url: str):
        """Open url in browser"""
