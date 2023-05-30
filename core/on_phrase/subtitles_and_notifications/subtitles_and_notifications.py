from talon import Module, ui, cron
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from talon.types import Rect
from typing import Type, Callable, Optional

mod = Module()
subtitle_canvas = []
notify_canvas = []
show_override = None


def setting(
    name: str, type: Type, desc: str, default: Optional[any] = None
) -> Callable[[bool], Type]:
    setting_subtitle = mod.setting(
        f"subtitles_{name}", type, default=default, desc=f"Subtitles: {desc}"
    )
    setting_notify = mod.setting(
        f"notifications_{name}", type, default=default, desc=f"Notifications: {desc}"
    )

    def callback(is_subtitle: bool):
        if is_subtitle:
            return setting_subtitle.get()
        return setting_notify.get()

    return callback


setting_show = setting("show", bool, "If true show")
setting_all_screens = setting(
    "all_screens", bool, "If true show on all screens instead of just the main screen"
)
setting_color = setting("color", str, "Text color")
setting_color_outline = setting("color_outline", str, "Text outline color")
setting_timeout_per_char = setting(
    "timeout_per_char", int, "Number of milliseconds to show text for each character"
)
setting_timeout_min = setting(
    "timeout_min", int, "Minimum number of milliseconds to show text for"
)
setting_timeout_max = setting(
    "timeout_max", int, "Maximum number of milliseconds to show text for"
)
setting_y = setting(
    "y", float, "Center Y-position in percentages(0-1). 0=top, 1=bottom"
)


def show_subtitle(text: str):
    """Show subtitle"""
    # Override take precedence
    if show_override is not None:
        if show_override:
            show_text(text, is_subtitle=True)
    else:
        possibly_show_text(text, is_subtitle=True)


@mod.action_class
class Actions:
    def toggle_subtitles():
        """Toggle subtitles"""
        global show_override
        show_override = not show_override

    def notify(text: str):
        """Show notification"""
        possibly_show_text(text, is_subtitle=False)

    def clear_subtitles():
        """Clear all current subtitles and notifications"""
        clear_canvases(subtitle_canvas)
        clear_canvases(notify_canvas)


def possibly_show_text(text: str, is_subtitle: bool):
    if setting_show(is_subtitle):
        show_text(text, is_subtitle)


def show_text(text: str, is_subtitle: bool):
    canvases = subtitle_canvas if is_subtitle else notify_canvas
    clear_canvases(canvases)
    if setting_all_screens(is_subtitle):
        screens = ui.screens()
    else:
        screens = [ui.main_screen()]
    for screen in screens:
        canvas = show_text_on_screen(screen, text, is_subtitle)
        canvases.append(canvas)


def show_text_on_screen(screen: ui.Screen, text: str, is_subtitle: bool):
    timeout = calculate_timeout(text, is_subtitle)
    canvas = Canvas.from_screen(screen)
    canvas.register("draw", lambda c: on_draw(c, text, is_subtitle))
    canvas.freeze()
    cron.after(f"{timeout}ms", canvas.close)
    return canvas


def on_draw(c: SkiaCanvas, text: str, is_subtitle: bool):
    # The min(width, height) is to not get gigantic size on portrait height
    size = min(c.width, c.height)
    rect = set_text_size_and_get_rect(c, size, text)
    x = c.rect.center.x - rect.center.x
    # Clamp coordinate to make sure entire text is visible
    y = max(
        min(
            c.rect.y + setting_y(is_subtitle) * c.rect.height + c.paint.textsize / 2,
            c.rect.bot - rect.bot,
        ),
        c.rect.top - rect.top,
    )

    c.paint.imagefilter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.style = c.paint.Style.FILL
    c.paint.color = setting_color(is_subtitle)
    c.draw_text(text, x, y)

    # Outline
    c.paint.imagefilter = None
    c.paint.style = c.paint.Style.STROKE
    c.paint.color = setting_color_outline(is_subtitle)
    c.draw_text(text, x, y)


def calculate_timeout(text: str, is_subtitle: bool) -> int:
    ms_per_char = setting_timeout_per_char(is_subtitle)
    ms_min = setting_timeout_min(is_subtitle)
    ms_max = setting_timeout_max(is_subtitle)
    return min(ms_max, max(ms_min, len(text) * ms_per_char))


def set_text_size_and_get_rect(c: SkiaCanvas, height: int, text: str) -> Rect:
    height_div = 14
    while True:
        c.paint.textsize = round(height / height_div)
        rect = c.paint.measure_text(text)[1]
        if rect.width < c.width * 0.75:
            return rect
        height_div += 2


def clear_canvases(canvas_list: list[Canvas]):
    for canvas in canvas_list:
        canvas.close()
    canvas_list.clear()
