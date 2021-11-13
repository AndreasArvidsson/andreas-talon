from talon import Module, actions, ui, cron
from talon.canvas import Canvas
from talon.skia import Paint as Paint
from talon.skia.imagefilter import ImageFilter as ImageFilter

mod = Module()
subtitles_all_screens_setting = mod.setting(
    "subtitles_all_screens", bool, default=False
)
subtitle_canvas = []
info_canvas = []


@mod.action_class
class Actions:
    def screens_show_numbering():
        """Show screen number on each screen"""
        number = 1
        for screen in ui.screens():
            show_screen_number(screen, number)
            number += 1

    def screens_get_by_number(screen_number: int) -> ui.Screen:
        """Get screen by number"""
        screens = ui.screens()
        length = len(screens)
        if screen_number < 1 or screen_number > length:
            raise Exception(
                f"Non-existing screen {screen_number} in range [1, {length}]"
            )
        return screens[screen_number - 1]

    def subtitle(text: str):
        """Show subtitle"""
        show_subtitle(subtitle_canvas, text, info=False)

    def notify(text: str):
        """Show notification"""
        show_subtitle(info_canvas, text, info=True)


def show_subtitle(canvas_list: list, text: str, info: bool):
    for canvas in canvas_list:
        canvas.close()
    canvas_list.clear()
    if subtitles_all_screens_setting.get():
        screens = ui.screens()
    else:
        screens = [ui.main_screen()]
    for screen in screens:
        canvas = show_subtitle_on_screen(screen, text, info)
        canvas_list.append(canvas)


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


def show_subtitle_on_screen(screen: ui.Screen, text: str, info: bool):
    def on_draw(c):
        # The min(width, height) is to not get gigantic size on portrait height
        height = min(c.width, c.height)
        rect = set_subtitle_height_and_get_rect(c, height, text)
        x = c.x + c.width / 2 - rect.x - rect.width / 2
        if info:
            y = c.y + c.height / 2 + rect.height / 2
        else:
            y = c.y + c.height - round(height / 20)
        draw_text(c, text, x, y, info)
        timeout = max(750, len(text) * 50)
        if info:
            timeout *= 2
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


def draw_text(c, text: str, x: int, y: int, info: bool = False):
    filter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.imagefilter = filter

    c.paint.style = c.paint.Style.FILL
    c.paint.color = "6495ED" if info else "ffffff"
    c.draw_text(text, x, y)

    if not info:
        # Border / outline
        c.paint.imagefilter = None
        c.paint.style = c.paint.Style.STROKE
        c.paint.color = "aaaaaa"
        c.draw_text(text, x, y)
