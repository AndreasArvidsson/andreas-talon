from talon import Context, Module, actions, app, cron, ctrl, noise, ui
from talon_plugins import eye_mouse
from talon_plugins.eye_mouse import config, toggle_control

mod = Module()
ctx = Context()

mod.list("mouse_click", desc="Available mouse clicks")
ctx.lists["self.mouse_click"] = {
    "left":    "left",
    "right":   "right",
    "middle":  "middle",
    "mid":     "middle",
    "double":  "double",
    "dub":     "double",
    "triple":  "triple",
    "touch":   "touch"
}

scroll_job = None
gaze_job = None
scroll_speed = 100
scroll_dir = 1
scroll_step = 120
mouse_control = False
zoom_control = False


def on_pop(active: bool):
    # Do nothing if speech is disabled
    if not actions.speech.enabled():
        return
    stop_scroll()
    # Zoom mouse is enabled
    if actions.user.zoom_mouse_enabled():
        actions.user.zoom_mouse_on_pop()
    # Normal click
    else:
        ctrl.mouse_click(button=0)


noise.register("pop", on_pop)


@mod.action_class
class Actions:
    def mouse_click(action: str):
        """Click mouse button"""
        stop_scroll()
        if action == "left":
            ctrl.mouse_click(button=0)
        elif action == "right":
            ctrl.mouse_click(button=1)
        elif action == "middle":
            ctrl.mouse_click(button=2)
        elif action == "double":
            ctrl.mouse_click(button=0)
            ctrl.mouse_click(button=0)
        elif action == "triple":
            ctrl.mouse_click(button=0)
            ctrl.mouse_click(button=0)
            ctrl.mouse_click(button=0)

    def mouse_stop():
        """Stops mouse action"""
        # Close zoomed in view
        if not actions.user.zoom_mouse_idle():
            actions.user.zoom_mouse_cancel()
            return True
        # Stop scroll
        if scroll_job or gaze_job:
            stop_scroll()
            return True
        return False

    def mouse_drag():
        """Press and hold/release button 0 depending on state for dragging"""
        if 0 in ctrl.mouse_buttons_down():
            ctrl.mouse_click(button=0, up=True)
        else:
            ctrl.mouse_click(button=0, down=True)

    def mouse_scroll(direction: str, times: int):
        """Scrolls"""
        amount = scroll_step * times
        if direction == "up":
            amount = -amount
        actions.mouse_scroll(y=amount)

    def mouse_scrolling(direction: str):
        """Starts scrolling continuously"""
        global scroll_job, scroll_dir
        if direction == "up":
            scroll_dir = -1
        else:
            scroll_dir = 1
        if scroll_job is None:
            scroll_continuous_helper()
            scroll_job = cron.interval("30ms", scroll_continuous_helper)

    def mouse_scroll_speed(speed: int):
        """Set scroll speed"""
        if speed > 50:
            speed = 50
        global scroll_speed
        scroll_speed = speed * 10
        actions.user.mouse_print_scroll_speed()

    def mouse_scroll_increase():
        """Increase scroll speed"""
        global scroll_speed
        scroll_speed = scroll_speed + 20
        actions.user.mouse_print_scroll_speed()

    def mouse_scroll_decrease():
        """Decrease scroll speed"""
        global scroll_speed
        scroll_speed = scroll_speed - 20
        actions.user.mouse_print_scroll_speed()

    def mouse_print_scroll_speed():
        """Get scroll speed"""
        app.notify("Mouse scroll speed:\n{}%".format(scroll_speed))

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global gaze_job
        stop_scroll()
        gaze_job = cron.interval("60ms", scroll_gaze_helper)

    def mouse_calibrate():
        """Start calibration"""
        eye_mouse.calib_start()

    def mouse_toggle_control_mouse():
        """Toggles control mouse"""
        global mouse_control
        mouse_control = not config.control_mouse
        toggle_control(mouse_control)

    def mouse_toggle_zoom_mouse():
        """Toggles zoom mouse"""
        global zoom_control
        zoom_control = actions.user.zoom_mouse_toggle()

    def mouse_wake():
        """Enable control mouse and zoom mouse to earlier state"""
        toggle_control(mouse_control)
        actions.user.zoom_mouse_toggle(zoom_control)

    def mouse_sleep():
        """Disables control mouse, zoom mouse and scroll"""
        stop_scroll()
        toggle_control(False)
        actions.user.zoom_mouse_toggle(False)
        if 0 in ctrl.mouse_buttons_down():
            ctrl.mouse_click(button=0, up=True)


def stop_scroll():
    global scroll_job, gaze_job
    if scroll_job:
        cron.cancel(scroll_job)
        scroll_job = None
    if gaze_job:
        cron.cancel(gaze_job)
        gaze_job = None


def scroll_continuous_helper():
    if actions.user.zoom_mouse_idle():
        p = scroll_speed / 100
        amount = p * scroll_dir * scroll_step / 20
        actions.mouse_scroll(by_lines=False, y=amount)


def scroll_gaze_helper():
    if actions.user.zoom_mouse_idle():
        x, y = ctrl.mouse_pos()

        # the rect for the window containing the mouse
        rect = None

        # on windows, check the active_window first since ui.windows() is not z-ordered
        if app.platform == "windows" and ui.active_window().rect.contains(x, y):
            rect = ui.active_window().rect
        else:
            windows = ui.windows()
            for w in windows:
                if w.rect.contains(x, y):
                    rect = w.rect
                    break

        if rect is None:
            return

        midpoint = rect.y + rect.height / 2
        amount = int(((y - midpoint) / (rect.height / 10)) ** 3)
        actions.mouse_scroll(by_lines=False, y=amount)
