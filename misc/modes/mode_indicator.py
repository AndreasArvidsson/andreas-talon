from talon import app, registry, scope, ui, Module
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from talon.screen import Screen
from talon.ui import Rect

mod = Module()
setting = mod.setting("mode_indicator_show", bool, default=False)
current_color = ""
canvas: Canvas = None


def get_color() -> str:
    modes = scope.get("mode")
    if "sleep" in modes:
        return "808080"  # Grey
    if "dictation" in modes:
        return "da70d6"  # Orchid
    return "f8f8ff"  # GhostWhite


def draw(c: SkiaCanvas):
    c.paint.style = c.paint.Style.FILL
    c.paint.color = current_color + "aa"
    c.paint.imagefilter = ImageFilter.drop_shadow(1, 1, 1, 1, "000000")
    radius = c.rect.height / 2
    c.draw_circle(c.rect.center.x, c.rect.top + radius, radius)


def open():
    global canvas
    screen: Screen = ui.main_screen()
    radius = screen.dpi / 10
    side = radius * 2
    rect = Rect(screen.rect.center.x - radius, screen.rect.top, side, side)
    canvas = Canvas.from_rect(rect)
    canvas.register("draw", draw)
    canvas.freeze()


def close():
    global canvas
    canvas.unregister("draw", draw)
    canvas.close()
    canvas = None


def update_current_color():
    global current_color
    mode = get_color()
    if current_color != mode:
        current_color = mode
        canvas.freeze()


def update_contexts():
    if setting.get():
        if canvas is None:
            open()
        update_current_color()
    elif canvas is not None:
        close()


def on_ready():
    registry.register("update_contexts", update_contexts)


app.register("ready", on_ready)
