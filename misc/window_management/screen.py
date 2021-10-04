from talon import Module, actions, ui, cron
from talon.canvas import Canvas
from talon.skia import Paint as Paint
from talon.skia.imagefilter import ImageFilter as ImageFilter

mod = Module()
subtitles_all_screens_setting = mod.setting("subtitles_all_screens", bool, default=False)
subtitle_canvas = []


@mod.action_class
class Actions:
    def screens_show_numbering():
        """Show screen number on each screen"""
        screens = get_sorted_screens()
        number = 1
        for screen in screens:
            show_screen_number(screen, number)
            number += 1

    def screens_get_by_number(screen_number: int) -> ui.Screen:
        """Get screen by number"""
        screens = get_sorted_screens()
        length = len(screens)
        if screen_number < 1 or screen_number > length:
            raise Exception(
                f"Non-existing screen {screen_number} in range [1, {length}]"
            )
        return screens[screen_number - 1]

    def screens_get_previous(screen: ui.Screen) -> ui.Screen:
        """Get the screen before this one"""
        return get_screen_by_offset(screen, -1)

    def screens_get_next(screen: ui.Screen) -> ui.Screen:
        """Get the screen after this one"""
        return get_screen_by_offset(screen, 1)

    def screens_show_subtitle(text: str):
        """Show subtitle on all screens"""
        global subtitle_canvas
        for canvas in subtitle_canvas:
            canvas.close()
        subtitle_canvas = []
        screens = ui.screens() if subtitles_all_screens_setting.get() else [ui.main_screen()]
        for screen in screens:
            canvas = show_subtitle_on_screen(screen, text)
            subtitle_canvas.append(canvas)


def get_screen_by_offset(screen: ui.Screen, offset: int) -> ui.Screen:
    screens = get_sorted_screens()
    index = (screens.index(screen) + offset) % len(screens)
    return screens[index]


def get_sorted_screens():
    """Return screens sorted by their topmost, then leftmost, edge.
    Screens will be sorted leftto-right, then top-to-bottom as a tiebreak.
    """
    return sorted(
        sorted(ui.screens(), key=lambda screen: screen.visible_rect.top),
        key=lambda screen: screen.visible_rect.left,
    )


def show_screen_number(screen: ui.Screen, number: int):
    def on_draw(c):
        c.paint.typeface = "arial"
        # The min(width, height) is to not get gigantic size on portrait screens
        height = min(c.width, c.height)
        c.paint.textsize = round(height / 2)
        text = f"{number}"
        rect = c.paint.measure_text(text)[1]
        x = c.x + c.width / 2 - rect.x - rect.width / 2
        y = c.y + c.height / 2 + rect.height / 2
        draw_text(c, text, x, y)
        cron.after("3s", canvas.close)

    canvas = Canvas.from_rect(screen.rect)
    canvas.register("draw", on_draw)
    canvas.freeze()


def show_subtitle_on_screen(screen: ui.Screen, text: str):
    def on_draw(c):
        # The min(width, height) is to not get gigantic size on portrait height
        height = min(c.width, c.height)
        rect = set_subtitle_height_and_get_rect(c, height, text)
        x = c.x + c.width / 2 - rect.x - rect.width / 2
        y = c.y + c.height - round(height / 20)
        draw_text(c, text, x, y)
        timeout = max(750, len(text) * 50)
        cron.after(f"{timeout}ms", canvas.close)

    canvas = Canvas.from_rect(screen.rect)
    canvas.register("draw", on_draw)
    canvas.freeze()
    return canvas


def set_subtitle_height_and_get_rect(c, height: int, text: str):
    height_div = 14
    while True:
        c.paint.textsize = round(height / height_div)
        rect = c.paint.measure_text(text)[1]
        if rect.width < c.width * 0.75:
            return rect
        height_div += 2


def draw_text(c, text: str, x: int, y: int):
    filter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.imagefilter = filter

    c.paint.style = c.paint.Style.FILL
    c.paint.color = "ffffff"
    c.draw_text(text, x, y)

    # Border / outline
    c.paint.imagefilter = None
    c.paint.style = c.paint.Style.STROKE
    c.paint.color = "aaaaaa"
    c.draw_text(text, x, y)
