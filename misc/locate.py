from talon import Module, actions, ui, ctrl
from talon.experimental.locate import locate
import time

mod = Module()


@mod.action_class
class Actions:
    def locate_hover(name: str) -> tuple[bool, int, int]:
        """Hover image"""
        path = f"{actions.path.talon_user()}/andreas/images/{name}"
        rect = ui.active_window().rect
        t1 = time.perf_counter()
        locations = locate(path, rect=rect, threshold=0.99)
        print(f"{time.perf_counter() - t1:0.3}s")
        print(f"{len(locations)}x")

        if len(locations) == 0:
            return False, 0, 0

        location = locations[0]
        x = round(rect.x + location.x + location.width / 2)
        y = round(rect.y + location.y + location.height / 2)
        ctrl.mouse_move(x, y)
        return True, x, y

    def locate_click(name: str) -> tuple[bool, int, int]:
        """Locate image and mouse left click"""
        ok, x, y = actions.user.locate_hover(name)
        if ok:
            ctrl.mouse_click(button=0)
        return ok, x, y

    def locate_drag(name: str) -> tuple[bool, int, int]:
        """Locate image and mouse left click drag"""
        ok, x, y = actions.user.locate_hover(name)
        if ok:
            ctrl.mouse_click(button=0, down=True)
        return ok, x, y

    def locate_line_move(direction: int):
        """Move line"""
        ok, x, y = actions.user.locate_drag("line_vertical.png")
        if ok:
            actions.sleep(0.2)
            ctrl.mouse_move(x + 100 * direction, y)
            actions.sleep(0.2)
            ctrl.mouse_click(button=0, up=True)
