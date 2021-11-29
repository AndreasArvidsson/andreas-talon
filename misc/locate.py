from talon import Module, actions, ui, ctrl
from talon.experimental.locate import locate
import time

mod = Module()


@mod.action_class
class Actions:
    def locate_hover(name: str, filter_cb: callable = None) -> tuple[bool, int, int]:
        """Locate image and hover"""
        path = f"{actions.path.talon_user()}/andreas/images/{name}"
        rect = ui.active_window().rect
        t1 = time.perf_counter()
        locations = locate(path, rect=rect, threshold=0.99)
        print(f"locate: {time.perf_counter() - t1:0.3}s")

        if filter_cb:
            locations = list(filter(filter_cb, locations))

        if not locations:
            return False, 0, 0

        location = locations[0]
        x = rect.x + location.x + location.width / 2
        y = rect.y + location.y + location.height / 2
        ctrl.mouse_move(x, y)
        return True, x, y

    def locate_click(name: str, filter_cb: callable = None) -> tuple[bool, int, int]:
        """Locate image and mouse left click"""
        ok, x, y = actions.user.locate_hover(name, filter_cb)
        if ok:
            ctrl.mouse_click(button=0)
        return ok, x, y

    def locate_drag(name: str, filter_cb: callable = None) -> tuple[bool, int, int]:
        """Locate image and mouse left click drag"""
        ok, x, y = actions.user.locate_hover(name, filter_cb)
        if ok:
            ctrl.mouse_click(button=0, down=True)
        return ok, x, y
