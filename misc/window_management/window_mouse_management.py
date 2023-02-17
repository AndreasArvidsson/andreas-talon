from talon import ui, Module, actions
from dataclasses import dataclass

mod = Module()


@dataclass
class Side:
    side: str
    value: int
    distance: int


@mod.action_class
class Actions:
    def resize_window_at_cursor_position():
        """Resize active windows closest side to cursor position"""
        window = ui.active_window()
        x, y = actions.user.mouse_pos()
        side = get_closest_side(window, x, y)
        rect = window.rect

        if side.side == "left":
            pos = (x, rect.y, rect.right - x, rect.height)
        elif side.side == "right":
            pos = (rect.x, rect.y, x - rect.left, rect.height)
        elif side.side == "top":
            pos = (rect.x, y, rect.width, rect.bot - y)
        elif side.side == "bot":
            pos = (rect.x, rect.y, rect.width, y - rect.top)
        else:
            raise Exception(f"Unknown side {side.side}")

        actions.user.window_set_pos(window, *pos)

    def move_window_at_cursor_position():
        """Move active windows closest side to cursor position"""
        window = ui.active_window()
        x, y = actions.user.mouse_pos()
        side = get_closest_side(window, x, y)
        rect = window.rect

        if side.side == "left":
            pos = (x, rect.y, rect.width, rect.height)
        elif side.side == "right":
            pos = (x - rect.width, rect.y, rect.width, rect.height)
        elif side.side == "top":
            pos = (rect.x, y, rect.width, rect.height)
        elif side.side == "bot":
            pos = (rect.x, y - rect.height, rect.width, rect.height)
        else:
            raise Exception(f"Unknown side {side.side}")

        actions.user.window_set_pos(window, *pos)


def get_closest_side(window: ui.Window, x: float, y: float) -> Side:
    sides = []

    sides.append(Side("left", window.rect.left, abs(x - window.rect.left)))
    sides.append(Side("right", window.rect.right, abs(x - window.rect.right)))
    sides.append(Side("top", window.rect.top, abs(y - window.rect.top)))
    sides.append(Side("bot", window.rect.bot, abs(y - window.rect.bot)))

    sides.sort(key=lambda side: side.distance)

    return sides[0]
