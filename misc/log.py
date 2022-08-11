from talon import Module

mod = Module()


@mod.action_class
class Actions:
    def debug(message: str):
        """Log debug message"""
        print(f"DEBUG: {message}")
