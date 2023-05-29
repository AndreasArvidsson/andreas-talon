from talon import Module, ui, cron
from talon.canvas import Canvas
from talon.skia.imagefilter import ImageFilter

mod = Module()


@mod.action_class
class Actions:
    def screens_show_numbering():
        """Show screen number on each screen"""
        for i, screen in enumerate(ui.screens()):
            show_screen_number(screen, i + 1)

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


def draw_text(c, text: str, x: int, y: int):
    c.paint.imagefilter = ImageFilter.drop_shadow(2, 2, 1, 1, "000000")
    c.paint.style = c.paint.Style.FILL
    c.paint.color = "ffffff"
    c.draw_text(text, x, y)

    # Border / outline
    c.paint.imagefilter = None
    c.paint.style = c.paint.Style.STROKE
    c.paint.color = "aaaaaa"
    c.draw_text(text, x, y)
