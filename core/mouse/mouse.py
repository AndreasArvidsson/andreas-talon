from talon import Context, Module, actions, ui, ctrl

mod = Module()
ctx = Context()

mod.list("mouse_click", "Available mouse clicks")
ctx.lists["user.mouse_click"] = {
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


@mod.action_class
class Actions:
    def mouse_on_pop():
        """Mouse on pop handler"""
        actions.skip()

    def mouse_click(action: str):
        """Click mouse button"""
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
            actions.user.mouse_move_center_window()
            actions.mouse_click()

    def mouse_click_with_conditions():
        """Click left mouse button. If scrolling or dragging, stop instead."""
        # Stop scrolling
        stop_scroll = actions.user.mouse_scroll_stop()
        # Release any held mouse buttons
        stop_drag = actions.user.mouse_release_held_buttons()
        # Normal left click
        if not stop_scroll and not stop_drag:
            actions.mouse_click()

    def mouse_move_center_window():
        """Move the mouse cursor to the center of the active window"""
        rect = ui.active_window().rect
        actions.mouse_move(rect.center.x, rect.center.y)

    def mouse_release_held_buttons() -> bool:
        """Release held mouse buttons"""
        buttons = ctrl.mouse_buttons_down()
        if buttons:
            for button in buttons:
                actions.mouse_release(button)
            return True
        return False
