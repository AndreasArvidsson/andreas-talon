from talon import ui, Module, Context, actions
from dataclasses import dataclass


@dataclass
class RelativePosition:
    """Represents a window position as a fraction of the screen."""

    left: float
    top: float
    right: float
    bottom: float


@dataclass
class ScreenDesc:
    """Represents a single screen"""

    value: int
    offset: bool


snap_positions = {
    # Halves
    # .---.---.     .-------.
    # |   |   |  &  |-------|
    # '---'---'     '-------'
    "left": RelativePosition(0, 0, 0.5, 1),
    "right": RelativePosition(0.5, 0, 1, 1),
    "top": RelativePosition(0, 0, 1, 0.5),
    "bottom": RelativePosition(0, 0.5, 1, 1),
    # Thirds
    # .--.--.--.
    # |  |  |  |
    # '--'--'--'
    "center small": RelativePosition(1 / 3, 0, 2 / 3, 1),
    "left small": RelativePosition(0, 0, 1 / 3, 1),
    "right small": RelativePosition(2 / 3, 0, 1, 1),
    "left large": RelativePosition(0, 0, 2 / 3, 1),
    "right large": RelativePosition(1 / 3, 0, 1, 1),
    # Quarters
    # .---.---.
    # |---|---|
    # '---'---'
    "top left": RelativePosition(0, 0, 0.5, 0.5),
    "top right": RelativePosition(0.5, 0, 1, 0.5),
    "bottom left": RelativePosition(0, 0.5, 0.5, 1),
    "bottom right": RelativePosition(0.5, 0.5, 1, 1),
    # Sixths
    # .--.--.--.
    # |--|--|--|
    # '--'--'--'
    "top left small": RelativePosition(0, 0, 1 / 3, 0.5),
    "top right small": RelativePosition(2 / 3, 0, 1, 0.5),
    "top left large": RelativePosition(0, 0, 2 / 3, 0.5),
    "top right large": RelativePosition(1 / 3, 0, 1, 0.5),
    "top center small": RelativePosition(1 / 3, 0, 2 / 3, 0.5),
    "bottom left small": RelativePosition(0, 0.5, 1 / 3, 1),
    "bottom right small": RelativePosition(2 / 3, 0.5, 1, 1),
    "bottom left large": RelativePosition(0, 0.5, 2 / 3, 1),
    "bottom right large": RelativePosition(1 / 3, 0.5, 1, 1),
    "bottom center small": RelativePosition(1 / 3, 0.5, 2 / 3, 1),
    # Special
    "center": RelativePosition(1 / 6, 0, 5 / 6, 1),
    "top center": RelativePosition(1 / 6, 0, 5 / 6, 0.5),
    "bottom center": RelativePosition(1 / 6, 0.5, 5 / 6, 1),
    "middle": RelativePosition(1 / 6, 1 / 8, 5 / 6, 1),
    "full": RelativePosition(0, 0, 1, 1),
}

mod = Module()
ctx = Context()

mod.list(
    "window_snap_position",
    "Predefined window positions for the current window. See `RelativePosition`.",
)
ctx.lists["user.window_snap_position"] = snap_positions.keys()


@mod.capture(rule="screen (last|next|<number_small>)")
def screen(m) -> ScreenDesc:
    "A single screen position."
    try:
        return ScreenDesc(m.number_small, False)
    except AttributeError:
        return ScreenDesc(-1 if m[1] == "last" else 1, True)


@mod.action_class
class Actions:
    def window_snap_to_position(pos_name: str):
        """Move the active window to a specific position on the same screen"""
        snap_to_screen_and_position(ui.active_window().screen, pos_name)

    def window_snap_to_screen_and_position(screen_desc: ScreenDesc, pos_name: str):
        """Move the active window to a specific screen and position on that screen"""
        snap_to_screen_and_position(get_screen(screen_desc), pos_name)

    def window_snap_to_screen(screen_desc: ScreenDesc):
        """Move the active window to a specific screen and retaining the same relative position"""
        screen = get_screen(screen_desc)
        window = ui.active_window()
        dest = screen.visible_rect
        src = window.screen.visible_rect
        proportional_width = dest.width / src.width
        proportional_height = dest.height / src.height
        actions.user.window_set_pos(
            window,
            x=dest.left + (window.rect.left - src.left) * proportional_width,
            y=dest.top + (window.rect.top - src.top) * proportional_height,
            width=window.rect.width * proportional_width,
            height=window.rect.height * proportional_height,
        )

    def window_swap_positions_with_app(name: str):
        """Swap window position with application by name"""
        app = actions.user.get_app(name)
        activeWindow = ui.active_window()
        appWindow = app.windows()[0]
        if activeWindow != appWindow:
            activeRect = activeWindow.rect
            actions.user.window_set_rect(activeWindow, appWindow.rect)
            actions.user.window_set_rect(appWindow, activeRect)


def snap_to_screen_and_position(screen: ui.Screen, pos_name: str):
    pos = snap_positions[pos_name]
    window = ui.active_window()
    rect = screen.visible_rect
    actions.user.window_set_pos(
        window,
        x=rect.x + (rect.width * pos.left),
        y=rect.y + (rect.height * pos.top),
        width=rect.width * (pos.right - pos.left),
        height=rect.height * (pos.bottom - pos.top),
    )


def get_screen(screen_desc: ScreenDesc) -> ui.Screen:
    if screen_desc.offset:
        return actions.user.screen_get_by_offset(screen_desc.value)
    return actions.user.screen_get_by_number(screen_desc.value)
