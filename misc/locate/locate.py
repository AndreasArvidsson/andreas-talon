from talon import Module, actions, ui, ctrl
from talon.experimental.locate import locate
import time

mod = Module()


@mod.action_class
class Actions:
    def locate_hover(name: str) -> tuple[int, int]:
        """Hover image"""
        path = f"{actions.path.talon_user()}/andreas/images/{name}"
        rect = ui.active_window().rect
        t1 = time.perf_counter()
        locations = locate(path, rect=rect, threshold=0.99)
        print(f"{time.perf_counter() - t1:0.3}s")
        print(f"{len(locations)}x")

        location = locations[0]
        x = round(rect.x + location.x + location.width / 2)
        y = round(rect.y + location.y + location.height / 2)
        ctrl.mouse_move(x, y)
        return x, y

    def locate_grab_line(direction: str) -> tuple[int, int]:
        """Locate and grab line"""
        x, y = actions.user.locate_hover(f"line_{direction}.png")
        ctrl.mouse_click(button=0, down=True)
        return x, y

    def locate_line_move(direction: int):
        """Move line"""
        x, y = actions.user.locate_grab_line("vertical")
        actions.sleep(0.2)
        ctrl.mouse_move(x + 100 * direction, y)
        actions.sleep(0.2)
        ctrl.mouse_click(button=0, up=True)

