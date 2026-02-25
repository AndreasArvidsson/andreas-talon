from talon import actions, ui, app
from talon.screen import Screen


def get_active_screen() -> Screen:
    try:
        return ui.active_window().screen
    except Exception as e:
        print(f"Error getting active screen, defaulting to main screen: {e}")
        return ui.main_screen()


def get_screen_scale(screen: Screen) -> float:
    imgui_scale: float = actions.settings.get("imgui.scale", 1)
    if app.platform == "mac":
        return imgui_scale
    return imgui_scale * screen.scale


class NotSetType:
    def __repr__(self) -> str:
        return "<argument not set>"


NOT_SET = NotSetType()
