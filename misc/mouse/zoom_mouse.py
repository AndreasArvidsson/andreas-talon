from talon import Module, Context, actions, noise, ctrl
from talon_plugins import eye_zoom_mouse

mod = Module()
ctx = Context()

mod.tag("zoom_mouse", "Indicates that zoom mouse is zoomed in")


next_action = None


@ctx.action_class("tracking")
class TrackingActions:
    def control_zoom_toggle(state: bool):
        actions.next(state)
        if state:
            # Unregistered zoom mouse built in pop event.
            noise.unregister("pop", eye_zoom_mouse.zoom_mouse.on_pop)
        else:
            actions.user.zoom_mouse_cancel()


@mod.action_class
class Actions:
    def zoom_mouse_idle() -> bool:
        """Returns true if zoom mouse is idle"""
        return eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_IDLE

    def zoom_mouse_cancel():
        """Cancel zoom mouse"""
        global next_action
        next_action = None
        cancel_zoom()

    def zoom_mouse_click(action: str):
        """Click mouse button with zoom mouse"""
        global next_action
        next_action = action
        actions.user.notify(action)

    def zoom_mouse_on_pop():
        """Zoom mouse on pop event"""
        global next_action

        # In idle about to enter zoom
        if actions.user.zoom_mouse_idle():
            enter_zoom()
            return

        # Already in zoom about to click
        cancel_zoom()
        if move_cursor():
            # Has an action to perform
            if next_action:
                actions.user.mouse_click(next_action)
            # Normal left click
            else:
                actions.user.mouse_click("left")
        next_action = None


def enter_zoom():
    actions.user.mouse_hide_cursor()
    ctx.tags = ["user.zoom_mouse"]
    actions.tracking.zoom()


def cancel_zoom():
    actions.tracking.zoom_cancel()
    ctx.tags = []
    actions.user.mouse_show_cursor()


def move_cursor():
    dot, origin = eye_zoom_mouse.zoom_mouse.get_pos()
    if not origin:
        return False
    ctrl.mouse_move(origin.x, origin.y)
    return True
