from typing import Literal, get_args

from talon import ui, Module, Context, actions
from talon.ui import BaseWindow

mod = Module()
ctx = Context()
window_states = {}

RESIZE_SIZE = Literal["small", "medium", "large"]

mod.list("resize_side", "Side of window to use for resizing")
mod.list("resize_direction", "Direction of window to use for resizing")
mod.list("resize_size", "Offset to use for resizing")
ctx.lists["user.resize_side"] = {"left", "top", "right", "bottom"}  # pyright: ignore[reportArgumentType]
ctx.lists["user.resize_direction"] = {"in", "out"}  # pyright: ignore[reportArgumentType]
ctx.lists["user.resize_size"] = set(get_args(RESIZE_SIZE))  # pyright: ignore[reportArgumentType]


@mod.action_class
class Actions:
    @staticmethod
    def window_set_rect(window: BaseWindow, rect: ui.Rect):
        """Update window position. Keeps track of old position to enable revert/undo"""
        window_states[window] = window.rect
        window.rect = rect

    @staticmethod
    def window_set_pos(
        window: BaseWindow,
        x: float,
        y: float,
        width: float,
        height: float,
    ):
        """Update window position. Keeps track of old position to enable revert/undo"""
        actions.user.window_set_rect(
            window,
            ui.Rect(round(x), round(y), round(width), round(height)),
        )

    def revert_active_window_position():
        """Revert active window to last position"""
        revert_window(ui.active_window())

    def revert_window_under_cursor_position():
        """Revert the window under the cursor to last position"""
        revert_window(actions.user.get_window_under_cursor())

    @staticmethod
    def revert_application_window_position(app_name: str):
        """Revert window for application <app_name> to last position"""
        revert_window(actions.user.get_app_window(app_name))

    def move_window_to_screen_center():
        """Move the active window to the center of the current screen"""
        window = ui.active_window()
        rect = window.rect
        screen = window.screen.visible_rect
        actions.user.window_set_pos(
            window,
            x=screen.center.x - rect.width / 2,
            y=screen.center.y - rect.height / 2,
            width=rect.width,
            height=rect.height,
        )

    @staticmethod
    def swap_active_window_position_with_application(app_name: str):
        """Swap active window position with application <app_name>"""
        app = actions.user.get_app(app_name)
        activeWindow = ui.active_window()
        appWindow = app.windows()[0]
        if activeWindow != appWindow:
            activeRect = activeWindow.rect
            actions.user.window_set_rect(activeWindow, appWindow.rect)
            actions.user.window_set_rect(appWindow, activeRect)

    @staticmethod
    def window_resize(side: str, direction: str, resize_size: RESIZE_SIZE):
        """Resize the active window"""
        window = ui.active_window()
        screen = window.screen.visible_rect
        screen_size = min(screen.width, screen.height)
        if resize_size == "small":
            step = 0.05 * screen_size
        elif resize_size == "medium":
            step = 0.1 * screen_size
        elif resize_size == "large":
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

        actions.user.window_set_pos(
            window,
            x=max(x, screen.x),
            y=max(y, screen.y),
            width=min(width, screen.width),
            height=min(height, screen.height),
        )


def revert_window(window: BaseWindow):
    old_rect = window_states.get(window)
    if old_rect:
        actions.user.window_set_rect(window, old_rect)
