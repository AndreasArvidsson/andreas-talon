from talon import ui, Module, Context, actions
from dataclasses import dataclass


@dataclass
class WindowState:
    old_rect: ui.Rect
    new_rect: ui.Rect


mod = Module()
ctx = Context()
window_states = {}

mod.list("resize_side", "Side of window to use for resizing")
mod.list("resize_direction", "Direction of window to use for resizing")
mod.list("resize_size", "Offset to use for resizing")
ctx.lists["user.resize_side"] = {"left", "top", "right", "bottom"}
ctx.lists["user.resize_direction"] = {"in", "out"}
ctx.lists["user.resize_size"] = {"small", "medium", "large"}


@mod.action_class
class Actions:
    def window_set_rect(window: ui.Window, rect: ui.Rect):
        """Update window position. Keeps track of old position to enable revert/undo"""
        old_rect = window.rect
        window.rect = rect
        window_states[window.id] = WindowState(old_rect, rect)

    def window_set_pos(
        window: ui.Window, x: float, y: float, width: float, height: float
    ):
        """Update window position. Keeps track of old position to enable revert/undo"""
        actions.user.window_set_rect(
            window,
            ui.Rect(round(x), round(y), round(width), round(height)),
        )

    def window_revert_rect():
        """Revert window position"""
        window = ui.active_window()
        if window.id in window_states:
            state = window_states[window.id]
            if state:
                window.rect = state.old_rect
                window_states[window.id] = WindowState(state.new_rect, state.old_rect)

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

        actions.user.window_set_pos(
            window,
            x=max(x, screen.x),
            y=max(y, screen.y),
            width=min(width, screen.width),
            height=min(height, screen.height),
        )
