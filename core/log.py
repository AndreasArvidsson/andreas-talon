from talon import Module, settings

mod = Module()

setting = "log_level"

mod.setting(setting, type=str, default="info")


@mod.action_class
class Actions:
    def debug(message: str):
        """Log debug message"""
        if settings.get(setting) == "debug":
            print(f"DEBUG: {message}")

    def info(message: str):
        """Log info message"""
        if settings.get(setting) in ["debug", "info"]:
            print(f"INFO: {message}")
