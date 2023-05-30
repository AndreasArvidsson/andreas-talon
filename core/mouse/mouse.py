from talon import Context, Module, actions, ui, ctrl

mod = Module()
ctx = Context()

mod.list("mouse_click", desc="Available mouse clicks")
ctx.lists["self.mouse_click"] = {
    "left": "left",
    "right": "right",
    "middle": "middle",
    "mid": "middle",
    "double": "double",
    "dub": "double",
    "triple": "triple",
    "trip": "triple",
    "control": "control",
    "troll": "control",
    "shift": "shift",
    "center": "center",
}


@ctx.action_class("main")
class MainActions:
    def mouse_click(button: int = 0):
        ctrl.mouse_click(button=button, hold=16000)


@ctx.action_class("user")
class UserActions:
    def mouse_on_pop():
        pass


@mod.action_class
class Actions:
    def mouse_on_pop():
        """Mouse on pop handler"""

    def mouse_click(action: str):
        """Click mouse button"""
        actions.user.mouse_scroll_stop_for_click()
        if action == "left":
            actions.mouse_click()
        elif action == "right":
            actions.mouse_click(1)
        elif action == "middle":
            actions.mouse_click(2)
        elif action == "double":
            actions.mouse_click()
            actions.mouse_click()
        elif action == "triple":
            actions.mouse_click()
            actions.mouse_click()
            actions.mouse_click()
        elif action == "control":
            actions.key("ctrl:down")
            actions.mouse_click()
            actions.key("ctrl:up")
        elif action == "shift":
            actions.key("shift:down")
            actions.mouse_click()
            actions.key("shift:up")
        elif action == "center":
            actions.user.mouse_center_window()
            actions.mouse_click()

    def mouse_pos() -> tuple[float, float]:
        """Mouse position (X, Y)"""
        return ctrl.mouse_pos()

    def mouse_drag():
        """Press and hold/release button 0 depending on state for dragging"""
        if 0 in ctrl.mouse_buttons_down():
            actions.mouse_release()
            actions.user.notify("Mouse drag: False")
        else:
            actions.mouse_drag()
            actions.user.notify("Mouse drag: True")

    def mouse_center_window():
        """Move the mouse cursor to the center of the currently active window"""
        rect = ui.active_window().rect
        actions.mouse_move(rect.center.x, rect.center.y)

    def mouse_release_held_buttons():
        """Release held mouse buttons"""
        for button in ctrl.mouse_buttons_down():
            actions.mouse_release(button)
