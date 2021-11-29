from talon import Module, actions, ui, ctrl
from talon.experimental.locate import locate

mod = Module()


@mod.action_class
class Actions:
    def locate_hover(name: str):
        """Hover image"""
        path = f"{actions.path.talon_user()}/andreas/images/{name}"
        rect = ui.active_window().rect
        locations = locate(path, rect=rect)

        for l in locations:
            print(f"{rect.x+l.x}, {rect.y+l.y}, {l.width}, {l.height}")

        location = locations[0]
        x = rect.x + location.x + location.width / 2
        y = rect.y + location.y + location.height / 2
        ctrl.mouse_move(x, y)
