from talon import ui, Module, actions
from talon.types import Rect
from dataclasses import dataclass

mod = Module()


@dataclass
class Side:
    side: str
    x: float
    y: float


@mod.action_class
class Actions:
    def move_window_side_to_cursor_position():
        """Move active windows closest side to cursor position"""
        window = ui.active_window()
        rect = window.rect
        x, y = actions.user.mouse_pos()
        side = get_closest_side(rect, x, y)

        if side == "left":
            pos = (x, rect.y, rect.width, rect.height)
        elif side == "right":
            pos = (x - rect.width, rect.y, rect.width, rect.height)
        elif side == "top":
            pos = (rect.x, y, rect.width, rect.height)
        elif side == "bot":
            pos = (rect.x, y - rect.height, rect.width, rect.height)
        elif side == "NOOP":
            return
        else:
            raise Exception(f"Unknown side {side}")

        actions.user.window_set_pos(window, *pos)

    def resize_window_side_to_cursor_position():
        """Resize active windows closest side to cursor position"""
        window = ui.active_window()
        rect = window.rect
        x, y = actions.user.mouse_pos()
        side = get_closest_side(rect, x, y)

        if side == "left":
            pos = (x, rect.y, rect.right - x, rect.height)
        elif side == "right":
            pos = (rect.x, rect.y, x - rect.left, rect.height)
        elif side == "top":
            pos = (rect.x, y, rect.width, rect.bot - y)
        elif side == "bot":
            pos = (rect.x, rect.y, rect.width, y - rect.top)
        elif side == "NOOP":
            return
        else:
            raise Exception(f"Unknown side {side}")

        actions.user.window_set_pos(window, *pos)


def get_closest_side(rect: Rect, x: float, y: float) -> str:
    if not rect.contains(x, y):
        # Between top and bottom
        if y > rect.top and y < rect.bot:
            return "left" if x < rect.left else "right"
        # Between left and right
        if x > rect.left and x < rect.right:
            return "top" if y < rect.bot else "bot"
        # Outside one of the corners.
        return "NOOP"

    sides = [
        Side("left", rect.left, rect.top + rect.height / 2),
        Side("right", rect.right, rect.top + rect.height / 2),
        Side("top", rect.left + rect.width / 2, rect.top),
        Side("bot", rect.left + rect.width / 2, rect.bot),
    ]

    sides.sort(key=lambda side: distance(x, y, side.x, side.y))

    return sides[0].side


def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
