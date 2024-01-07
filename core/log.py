from talon import Module, settings

mod = Module()

mod.setting("log_level", type=str, default="info")


def get_log_level():
    return settings.get("user.log_level")


@mod.action_class
class Actions:
    def debug(message: str):
        """Log debug message"""
        if get_log_level() == "debug":
            print(f"DEBUG: {message}")

    def info(message: str):
        """Log info message"""
        if get_log_level() in ["debug", "info"]:
            print(f"INFO: {message}")
