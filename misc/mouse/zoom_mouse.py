from talon import Module, Context, actions, noise, ctrl
from talon_plugins import eye_zoom_mouse

mod = Module()
ctx = Context()

mod.tag("zoom_mouse", "Indicates that zoom mouse is zoomed in")


next_action = None


@mod.action_class
class Actions:
    def zoom_mouse_toggle(enabled: bool = None) -> bool:
        """Toggle zoom mouse"""
        if enabled == None:
            enabled = not eye_zoom_mouse.zoom_mouse.enabled
        enabled = enabled and eye_zoom_mouse.tracker is not None
        eye_zoom_mouse.toggle_zoom_mouse(enabled)
        if enabled:
            # Unregistered zoom mouse built in pop event.
            noise.unregister("pop", eye_zoom_mouse.zoom_mouse.on_pop)
        else:
            actions.user.zoom_mouse_cancel()
        return enabled

    def zoom_mouse_enabled() -> bool:
        """Returns true if zoom mouse is enabled"""
        return eye_zoom_mouse.zoom_mouse.enabled

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
        if eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_IDLE:
            enter_zoom()
            return
        # Already in zoom about to click
        cancel_zoom()
        if move_cursor():
            # Left mouse button is held down: end drag
            if 0 in ctrl.mouse_buttons_down():
                actions.user.mouse_drag()
            # Has an action to perform
            elif next_action:
                actions.user.mouse_click(next_action)
            # Normal left click
            else:
                ctrl.mouse_click(button=0)
        next_action = None


def enter_zoom():
    actions.user.mouse_hide_cursor()
    ctx.tags = ["user.zoom_mouse"]
    eye_zoom_mouse.zoom_mouse.on_pop(True)


def cancel_zoom():
    eye_zoom_mouse.zoom_mouse.cancel()
    ctx.tags = []
    actions.user.mouse_show_cursor()


def move_cursor():
    dot, origin = eye_zoom_mouse.zoom_mouse.get_pos()
    if not origin:
        return False
    ctrl.mouse_move(origin.x, origin.y)
    return True
