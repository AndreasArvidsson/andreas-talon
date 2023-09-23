from talon import Module, actions, cron, ui
from talon.screen import Screen
import time

HOLD_TIMEOUT = 0.2

screen: Screen = ui.main_screen()
mod = Module()
cron_job = None
slow_scroll = False
slow_mouse_move = False
mouse_freeze_time = 0
_x = 0
_y = 0


@mod.action_class
class Actions:
    def gamepad_scroll(x: float, y: float):
        """Perform gamepad scrolling"""
        global cron_job, _x, _y
        multiplier = 1.5 if slow_scroll else 3
        _x = x**3 * multiplier
        _y = y**3 * multiplier

        if _x != 0 or _y != 0:
            if cron_job is None:
                cron_job = cron.interval("16ms", scroll_continuous_helper)
        elif cron_job is not None:
            cron.cancel(cron_job)
            cron_job = None

    def gamepad_mouse_move(dx: float, dy: float):
        """Perform gamepad mouse cursor movement"""
        multiplier = 0.15 if slow_mouse_move else 0.3
        x, y = actions.user.mouse_pos()
        screen = get_screen(x, y)
        dx = dx**3 * screen.dpi * multiplier
        dy = dy**3 * screen.dpi * multiplier
        actions.mouse_move(x + dx, y + dy)

    def gamepad_mouse_freeze(button_down: bool):
        """Toggle gamepad mouse freeze"""
        global mouse_freeze_time
        if button_down:
            mouse_freeze_time = time.perf_counter()
            actions.user.mouse_freeze_toggle()
        elif time.perf_counter() - mouse_freeze_time > HOLD_TIMEOUT:
            actions.user.mouse_freeze_toggle()

    def gamepad_scroll_slow_toggle():
        """Toggle gamepad slow scroll mode"""
        global slow_scroll
        slow_scroll = not slow_scroll
        # actions.user.notify(f"Gamepad slow scroll: {slow_scroll}")

    def gamepad_mouse_move_slow_toggle():
        """Toggle gamepad slow mouse move mode"""
        global slow_mouse_move
        slow_mouse_move = not slow_mouse_move
        # actions.user.notify(f"Gamepad slow move: {slow_move}")

    def gamepad_mouse_jump(direction: str):
        """Move the mouse cursor to the specified quadrant of the active screen"""
        x, y = actions.user.mouse_pos()
        rect = ui.screen_containing(x, y).rect

        # Half distance between cursor and screen edge
        match direction:
            case "up":
                y = rect.top + (y - rect.top) / 2
            case "down":
                y = rect.bot - (rect.bot - y) / 2
            case "left":
                x = rect.left + (x - rect.left) / 2
            case "right":
                x = rect.right - (rect.right - x) / 2

        # # Move one fourth of screen width/height
        # match direction:
        #     case "up":
        #         y -= rect.height / 4
        #     case "down":
        #         y += rect.height / 4
        #     case "left":
        #         x -= rect.width / 4
        #     case "right":
        #         x += rect.width / 4

        actions.mouse_move(x, y)


def scroll_continuous_helper():
    actions.mouse_scroll(x=_x, y=_y, by_lines=True)


def get_screen(x: float, y: float) -> Screen:
    global screen
    if not screen.contains(x, y):
        screen = ui.screen_containing(x, y)
    return screen
