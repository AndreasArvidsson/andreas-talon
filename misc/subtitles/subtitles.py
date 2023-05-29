from talon import Module, ui, cron
from talon.canvas import Canvas
from talon.skia.imagefilter import ImageFilter

mod = Module()
subtitle_canvas = []
notify_canvas = []
show_override = None

settings_show = mod.setting(
    "subtitles_show",
    bool,
    default=False,
    desc="If true show subtitles",
)
setting_all_screens = mod.setting(
    "subtitles_all_screens",
    bool,
    desc="If true show subtitles on all screens instead of just the main screen",
)
setting_color = mod.setting(
    "subtitles_color",
    str,
    desc="Subtitles color",
)
setting_color_notify = mod.setting(
    "subtitles_color_notify",
    str,
    desc="Notify color",
)
setting_color_border = mod.setting(
    "subtitles_color_border",
    float,
    desc="Subtitles/notifications border brightness in percentages(0-1). 0=darkest, 1=brightest",
)


@mod.action_class
class Actions:
    def toggle_subtitles():
        """Toggle subtitles"""
        global show_override
        show_override = not show_override

    def subtitle(text: str):
        """Show subtitle"""
        # Override take precedence
        if show_override is not None:
            if show_override:
                show_text(text, is_subtitle=True)
        elif settings_show.get():
            show_text(text, is_subtitle=True)

    def notify(text: str):
        """Show notification"""
        show_text(text, is_subtitle=False)

    def clear_subtitles():
        """Clear all current subtitles"""
        clear_canvases(subtitle_canvas)
        clear_canvases(notify_canvas)


def show_text(text: str, is_subtitle: bool):
    canvases = subtitle_canvas if is_subtitle else notify_canvas
    clear_canvases(canvases)
    if setting_all_screens.get():
        screens = ui.screens()
    else:
        screens = [ui.main_screen()]
    for screen in screens:
        canvas = show_text_on_screen(screen, text, is_subtitle)
        canvases.append(canvas)


def show_text_on_screen(screen: ui.Screen, text: str, is_subtitle: bool):
    def on_draw(c):
        # The min(width, height) is to not get gigantic size on portrait height
        height = min(c.width, c.height)
        rect = set_text_size_and_get_rect(c, height, text)
        x = c.rect.center.x - rect.center.x
        if is_subtitle:
            color = setting_color.get()
            y = c.y + c.height - round(height / 20)
        # Notify
        else:
            color = setting_color_notify.get()
            y = c.rect.center.y + rect.height / 2
        draw_text(c, text, x, y, color)
        timeout = min(5000, max(750, len(text) * 50))
        # Notify
        if not is_subtitle:
            timeout *= 2
        cron.after(f"{timeout}ms", canvas.close)

    canvas = Canvas.from_screen(screen)
    canvas.register("draw", on_draw)
    canvas.freeze()
    return canvas


def set_text_size_and_get_rect(c, height: int, text: str):
    height_div = 14
    while True:
        c.paint.textsize = round(height / height_div)
        rect = c.paint.measure_text(text)[1]
        if rect.width < c.width * 0.75:
            return rect
        height_div += 2


def draw_text(c, text: str, x: int, y: int, color: str):
    c.paint.imagefilter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.style = c.paint.Style.FILL
    c.paint.color = color
    c.draw_text(text, x, y)

    # Border / outline
    c.paint.imagefilter = None
    c.paint.style = c.paint.Style.STROKE
    c.paint.color = get_gradient_color(color)
    c.draw_text(text, x, y)


def clear_canvases(canvas_list: list[Canvas]):
    for canvas in canvas_list:
        canvas.close()
    canvas_list.clear()


def get_gradient_color(color: str) -> str:
    factor = setting_color_border.get()
    # hex -> rgb
    (r, g, b) = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
    # Darken rgb
    r, g, b = int(r * factor), int(g * factor), int(b * factor)
    # rgb -> hex
    return f"{r:02x}{g:02x}{b:02x}"
