from dataclasses import dataclass
from talon import ui, Module, Context, actions

mod = Module()
ctx = Context()
mod.list(
    "window_snap_position",
    "Predefined window positions for the current window. See `RelativeScreenPos`.",
)
mod.list("resize_side", "Side of window to use for resizing")
mod.list("resize_direction", "Direction of window to use for resizing")
mod.list("resize_size", "Offset to use for resizing")
ctx.lists["user.resize_side"] = {"left", "top", "right", "bottom"}
ctx.lists["user.resize_direction"] = {"in", "out"}
ctx.lists["user.resize_size"] = {"small", "medium", "large"}


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
    "middle": RelativeScreenPos(1 / 6, 1 / 6, 5 / 6, 5 / 6),
    "center": RelativeScreenPos(1 / 6, 0, 5 / 6, 1),
    "full": RelativeScreenPos(0, 0, 1, 1),
}

ctx.lists["user.window_snap_position"] = snap_positions.keys()


@mod.capture(rule="{user.window_snap_position}")
def window_snap_position(m) -> RelativeScreenPos:
    return snap_positions[m.window_snap_position]


@mod.action_class
class Actions:
    def snap_window(pos: RelativeScreenPos):
        """Move the active window to a specific position on-screen.
        See `RelativeScreenPos` for the structure of this position.
        """
        window = ui.active_window()
        screen = window.screen.visible_rect
        set_window_pos(
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

    def move_window_to_screen_center():
        """Move the active window to the center of the current screen"""
        window = ui.active_window()
        rect = window.rect
        screen = window.screen.visible_rect
        set_window_pos(
            window,
            x=screen.x + (screen.width / 2 - rect.width / 2),
            y=screen.y + (screen.height / 2 - rect.height / 2),
            width=rect.width,
            height=rect.height,
        )

    def resize_window(side: str, direction: str, offset: str):
        """Resize the active window"""
        window = ui.active_window()
        screen = window.screen.visible_rect
        screen_size = min(screen.width, screen.height)
        if offset == "small":
            step = 0.05 * screen_size
        elif offset == "medium":
            step = 0.1 * screen_size
        elif offset == "large":
            step = 0.2 * screen_size
        rect = window.rect
        x = rect.x
        y = rect.y
        width = rect.width
        height = rect.height
        increase = direction == "out"
        if side == "left":
            if increase:
                x -= step
                width += step
            else:
                x += step
                width -= step
        elif side == "top":
            if increase:
                y -= step
                height += step
            else:
                y += step
                height -= step
        elif side == "right":
            if increase:
                width += step
            else:
                width -= step
        elif side == "bottom":
            if increase:
                height += step
            else:
                height -= step

        set_window_pos(
            window,
            x=max(x, screen.x),
            y=max(y, screen.y),
            width=min(width, screen.width),
            height=min(height, screen.height),
        )


def set_window_pos(window: ui.Window, x, y, width, height):
    """Helper to set the window position."""
    window.rect = ui.Rect(round(x), round(y), round(width), round(height))


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

    set_window_pos(
        window,
        x=dest.left + (window.rect.left - src.left) * proportional_width,
        y=dest.top + (window.rect.top - src.top) * proportional_height,
        width=window.rect.width * proportional_width,
        height=window.rect.height * proportional_height,
    )
