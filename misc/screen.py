from talon import Module, ui, cron
from talon.canvas import Canvas
from talon.skia.imagefilter import ImageFilter

mod = Module()
show_subtitles = mod.setting("subtitles_show", bool, default=True).get()
subtitles_all_screens_setting = mod.setting(
    "subtitles_all_screens", bool, default=False
)
subtitle_canvas = []
notify_canvas = []


@mod.action_class
class Actions:
    def screens_show_numbering():
        """Show screen number on each screen"""
        number = 1
        for screen in ui.screens():
            show_screen_number(screen, number)
            number += 1

    def screen_get_by_number(screen_number: int) -> ui.Screen:
        """Get screen by number"""
        screens = ui.screens()
        length = len(screens)
        if screen_number < 1 or screen_number > length:
            raise Exception(
                f"Non-existing screen {screen_number} in range [1, {length}]"
            )
        return screens[screen_number - 1]

    def screen_get_by_offset(offset: int):
        """Get screen by offset"""
        screens = ui.screens()
        src_screen = ui.active_window().screen
        index = (screens.index(src_screen) + offset) % len(screens)
        return screens[index]

    def toggle_subtitles():
        """Toggle subtitles"""
        global show_subtitles
        show_subtitles = not show_subtitles

    def subtitle(text: str):
        """Show subtitle"""
        if show_subtitles:
            show_text(text, is_subtitle=True)

    def notify(text: str):
        """Show notification"""
        show_text(text, is_subtitle=False)

    def clear_subtitles():
        """Clear all current subtitles"""
        if show_subtitles:
            clear_subtitles(subtitle_canvas)
            clear_subtitles(notify_canvas)


def show_text(text: str, is_subtitle: bool):
    canvas_list = subtitle_canvas if is_subtitle else notify_canvas
    clear_subtitles(canvas_list)
    if subtitles_all_screens_setting.get():
        screens = ui.screens()
    else:
        screens = [ui.main_screen()]
    for screen in screens:
        canvas = show_text_on_screen(screen, text, is_subtitle)
        canvas_list.append(canvas)


def show_screen_number(screen: ui.Screen, number: int):
    def on_draw(c):
        c.paint.typeface = "arial"
        # The min(width, height) is to not get gigantic size on portrait screens
        height = min(c.width, c.height)
        c.paint.textsize = round(height / 2)
        text = f"{number}"
        rect = c.paint.measure_text(text)[1]
        x = c.rect.center.x - rect.center.x
        y = c.rect.center.y + rect.height / 2
        draw_text(c, text, x, y)
        cron.after("3s", canvas.close)

    canvas = Canvas.from_screen(screen)
    canvas.register("draw", on_draw)
    canvas.freeze()


def show_text_on_screen(screen: ui.Screen, text: str, is_subtitle: bool):
    def on_draw(c):
        # The min(width, height) is to not get gigantic size on portrait height
        height = min(c.width, c.height)
        rect = set_text_size_and_get_rect(c, height, text)
        x = c.rect.center.x - rect.center.x
        if is_subtitle:
            y = c.y + c.height - round(height / 20)
        # Notify
        else:
            y = c.rect.center.y + rect.height / 2
        draw_text(c, text, x, y, is_subtitle)
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


def draw_text(c, text: str, x: int, y: int, is_subtitle: bool = True):
    filter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.imagefilter = filter

    c.paint.style = c.paint.Style.FILL
    c.paint.color = "ffffff" if is_subtitle else "6495ED"
    c.draw_text(text, x, y)

    if is_subtitle:
        # Border / outline
        c.paint.imagefilter = None
        c.paint.style = c.paint.Style.STROKE
        c.paint.color = "aaaaaa"
        c.draw_text(text, x, y)


def clear_subtitles(canvas_list: list[Canvas]):
    for canvas in canvas_list:
        canvas.close()
    canvas_list.clear()
