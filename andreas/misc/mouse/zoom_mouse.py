from talon import Module, actions, noise, ctrl
from talon_plugins import eye_zoom_mouse

mod = Module()
next_action = None


@mod.action_class
class Actions:
    def zoom_mouse_toggle(enabled: bool = None) -> bool:
        """Toggle zoom mouse"""
        if enabled == None:
            enabled = not eye_zoom_mouse.zoom_mouse.enabled
        eye_zoom_mouse.toggle_zoom_mouse(enabled)
        if enabled:
            # Unregistered zoom mouse built in pop event.
            noise.unregister("pop", eye_zoom_mouse.zoom_mouse.on_pop)
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
        eye_zoom_mouse.zoom_mouse.cancel()
        actions.user.mouse_show_cursor()
        next_action = None

    def zoom_mouse_click(action: str):
        """Click mouse button with zoom mouse"""
        global next_action
        next_action = action

    def zoom_mouse_on_pop():
        """Zoom mouse on pop event"""
        global next_action
        # In idle about to enter zoom
        if (eye_zoom_mouse.zoom_mouse.state == eye_zoom_mouse.STATE_IDLE):
            actions.user.mouse_hide_cursor()
            eye_zoom_mouse.zoom_mouse.on_pop(True)
        # Already in zoom about to click
        else:
            actions.user.mouse_show_cursor()
            # Cancel zoom and move cursor to origin
            eye_zoom_mouse.zoom_mouse.cancel()
            dot, origin = eye_zoom_mouse.zoom_mouse.get_pos()
            if not origin:
                return
            ctrl.mouse_move(origin.x, origin.y)
            # Left mouse button is held down: end drag
            if 0 in ctrl.mouse_buttons_down():
                ctrl.mouse_click(button=0, up=True)
            # Has an action to perform
            elif next_action:
                actions.user.mouse_click(next_action, True)
                next_action = None
            # Normal left click
            else:
                ctrl.mouse_click(button=0)
