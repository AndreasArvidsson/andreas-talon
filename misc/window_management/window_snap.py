from talon import ui, Module, Context, actions
from dataclasses import dataclass


@dataclass
class RelativeScreenPos:
    """Represents a window position as a fraction of the screen."""

    left: float
    top: float
    right: float
    bottom: float


snap_positions = {
    # Halves
    # .---.---.     .-------.
    # |   |   |  &  |-------|
    # '---'---'     '-------'
    "left": RelativeScreenPos(0, 0, 0.5, 1),
    "right": RelativeScreenPos(0.5, 0, 1, 1),
    "top": RelativeScreenPos(0, 0, 1, 0.5),
    "bottom": RelativeScreenPos(0, 0.5, 1, 1),
    # Thirds
    # .--.--.--.
    # |  |  |  |
    # '--'--'--'
    "center small": RelativeScreenPos(1 / 3, 0, 2 / 3, 1),
    "left small": RelativeScreenPos(0, 0, 1 / 3, 1),
    "right small": RelativeScreenPos(2 / 3, 0, 1, 1),
    "left large": RelativeScreenPos(0, 0, 2 / 3, 1),
    "right large": RelativeScreenPos(1 / 3, 0, 1, 1),
    # Quarters
    # .---.---.
    # |---|---|
    # '---'---'
    "top left": RelativeScreenPos(0, 0, 0.5, 0.5),
    "top right": RelativeScreenPos(0.5, 0, 1, 0.5),
    "bottom left": RelativeScreenPos(0, 0.5, 0.5, 1),
    "bottom right": RelativeScreenPos(0.5, 0.5, 1, 1),
    # Sixths
    # .--.--.--.
    # |--|--|--|
    # '--'--'--'
    "top left small": RelativeScreenPos(0, 0, 1 / 3, 0.5),
    "top right small": RelativeScreenPos(2 / 3, 0, 1, 0.5),
    "top left large": RelativeScreenPos(0, 0, 2 / 3, 0.5),
    "top right large": RelativeScreenPos(1 / 3, 0, 1, 0.5),
    "top center small": RelativeScreenPos(1 / 3, 0, 2 / 3, 0.5),
    "bottom left small": RelativeScreenPos(0, 0.5, 1 / 3, 1),
    "bottom right small": RelativeScreenPos(2 / 3, 0.5, 1, 1),
    "bottom left large": RelativeScreenPos(0, 0.5, 2 / 3, 1),
    "bottom right large": RelativeScreenPos(1 / 3, 0.5, 1, 1),
    "bottom center small": RelativeScreenPos(1 / 3, 0.5, 2 / 3, 1),
    # Special
    "center": RelativeScreenPos(1 / 6, 0, 5 / 6, 1),
    "top center": RelativeScreenPos(1 / 6, 0, 5 / 6, 0.5),
    "bottom center": RelativeScreenPos(1 / 6, 0.5, 5 / 6, 1),
    "middle": RelativeScreenPos(1 / 6, 1 / 8, 5 / 6, 1),
    "full": RelativeScreenPos(0, 0, 1, 1),
}

mod = Module()
ctx = Context()

mod.list(
    "window_snap_position",
    "Predefined window positions for the current window. See `RelativeScreenPos`.",
)
ctx.lists["user.window_snap_position"] = snap_positions.keys()


@mod.action_class
class Actions:
    def snap_window(pos_name: str):
        """Move the active window to a specific position on-screen."""
        pos = snap_positions[pos_name]
        window = ui.active_window()
        screen = window.screen.visible_rect
        actions.user.window_set_pos(
            window,
            x=screen.x + (screen.width * pos.left),
            y=screen.y + (screen.height * pos.top),
            width=screen.width * (pos.right - pos.left),
            height=screen.height * (pos.bottom - pos.top),
        )

    def move_window_previous_screen():
        """Move the active window to the previous screen."""
        move_to_screen(ui.active_window(), offset=-1)

    def move_window_next_screen():
        """Move the active window to the next screen."""
        move_to_screen(ui.active_window(), offset=1)

    def move_window_to_screen(screen_number: int):
        """Move the active window to a specific screen."""
        move_to_screen(ui.active_window(), screen_number=screen_number)

    def swap_window_position(name: str):
        """Swap window position with application by name"""
        app = actions.user.get_app(name)
        activeWindow = ui.active_window()
        appWindow = app.windows()[0]
        if activeWindow != appWindow:
            activeRect = activeWindow.rect
            actions.user.window_set_rect(activeWindow, appWindow.rect)
            actions.user.window_set_rect(appWindow, activeRect)


def move_to_screen(window: ui.Window, offset: int = None, screen_number: int = None):
    """Move a window to a different screen.
    Provide one of `offset` or `screen_number` to specify a target screen.
    Provide `window` to move a specific window, otherwise the current window is
    moved.
    """
    assert (
        screen_number or offset and not (screen_number and offset)
    ), "Provide exactly one of `screen_number` or `offset`."

    src_screen = window.screen

    if offset:
        screens = ui.screens()
        index = (screens.index(src_screen) + offset) % len(screens)
        dest_screen = screens[index]
    else:
        dest_screen = actions.user.screens_get_by_number(screen_number)

    if src_screen == dest_screen:
        return

    # Retain the same proportional position on the new screen.
    dest = dest_screen.visible_rect
    src = src_screen.visible_rect
    proportional_width = dest.width / src.width
    proportional_height = dest.height / src.height

    actions.user.window_set_pos(
        window,
        x=dest.left + (window.rect.left - src.left) * proportional_width,
        y=dest.top + (window.rect.top - src.top) * proportional_height,
        width=window.rect.width * proportional_width,
        height=window.rect.height * proportional_height,
    )
