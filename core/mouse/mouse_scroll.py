from talon import Module, actions, app, ui, cron, settings, ctrl
from talon.canvas import Canvas
from talon.types import Rect
from talon.skia.canvas import Canvas as SkiaCanvas
from typing import Literal
import time

mod = Module()

mod.setting(
    "scroll_speed",
    type=float,
    default=1,
    desc="Base scroll speed",
)

gaze_canvas: Canvas | None = None
gaze_job = None
scroll_job = None
gaze_origin_y: float = 0
scroll_dir: Literal[-1, 1] = 1
scroll_ts: float = 0
scroll_speed: float = 0


@mod.action_class
class Actions:
    def mouse_scroll_stop():
        """Stop mouse scroll"""
        global scroll_job, gaze_job
        return_value = scroll_job or gaze_job
        if scroll_job:
            cron.cancel(scroll_job)
            scroll_job = None
        if gaze_job:
            cron.cancel(gaze_job)
            gaze_job = None
            hide_gaze_indicator()
        return return_value

    def mouse_scroll_up(times: int):
        """Scrolls"""
        y = times
        actions.mouse_scroll(-y, by_lines=True)

    def mouse_scroll_down(times: int):
        """Scrolls"""
        y = times
        actions.mouse_scroll(y, by_lines=True)

    def mouse_scroll_up_continuous():
        """Toggle scrolling down continuously"""
        mouse_scroll_continuous(-1)

    def mouse_scroll_down_continuous():
        """Toggle scrolling down continuously"""
        mouse_scroll_continuous(1)

    def mouse_gaze_scroll():
        """Starts gaze scroll"""
        global gaze_job, gaze_origin_y
        actions.user.mouse_scroll_stop()
        x, gaze_origin_y = ctrl.mouse_pos()
        show_gaze_indicator(x, gaze_origin_y)
        gaze_job = cron.interval("16ms", scroll_gaze_helper)


def mouse_scroll_continuous(new_scroll_dir: Literal[-1, 1]):
    global scroll_job, scroll_dir, scroll_ts, scroll_speed
    if scroll_job:
        # Issuing a scroll in the same direction aborts scrolling
        if scroll_dir == new_scroll_dir:
            cron.cancel(scroll_job)
            scroll_job = None
        # Issuing a scroll in the reverse direction resets acceleration
        else:
            scroll_dir = new_scroll_dir
            scroll_ts = time.perf_counter()
    else:
        scroll_dir = new_scroll_dir
        scroll_ts = time.perf_counter()
        scroll_speed = settings.get("user.scroll_speed")  # type: ignore
        scroll_continuous_helper()
        scroll_job = cron.interval("16ms", scroll_continuous_helper)


def scroll_continuous_helper():
    acceleration_speed = 1 + min((time.perf_counter() - scroll_ts) / 0.5, 4)
    scroll_speed: float = settings.get("user.scroll_speed", 0)  # type: ignore
    y = scroll_speed * acceleration_speed * scroll_dir
    actions.mouse_scroll(y, by_lines=True)


def scroll_gaze_helper():
    x, y = ctrl.mouse_pos()
    window = get_window_for_cursor(x, y)
    if window is None:
        return
    rect = window.rect
    y = ((y - gaze_origin_y) / (rect.height / 3)) ** 3
    actions.mouse_scroll(y, by_lines=True)


def get_window_for_cursor(x: float, y: float):
    # on windows, check the active_window first since ui.windows() is not z-ordered
    if app.platform == "windows" and ui.active_window().rect.contains(x, y):
        return ui.active_window()

    for window in ui.windows():
        if window.rect.contains(x, y):
            return window

    return None


def show_gaze_indicator(x: float, y: float):
    global gaze_canvas
    screen = ui.screen_containing(x, y)
    scale = screen.scale if app.platform != "mac" else 1
    size = 10 * scale
    gaze_canvas = Canvas.from_rect(
        Rect(
            x - size / 4,
            y - size / 2,
            size,
            size,
        )
    )
    gaze_canvas.register("draw", on_draw_gaze)


def hide_gaze_indicator():
    global gaze_canvas
    if gaze_canvas:
        gaze_canvas.unregister("draw", on_draw_gaze)
        gaze_canvas.close()
        gaze_canvas = None


def on_draw_gaze(c: SkiaCanvas):
    x, y = c.rect.center.x, c.rect.center.y
    radius = c.rect.height / 2 - 2
    c.paint.style = c.paint.Style.FILL
    c.paint.color = "red"
    c.draw_circle(x, y, radius)
