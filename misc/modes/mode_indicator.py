from talon import app, registry, scope, ui, Module
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from talon.screen import Screen
from talon.ui import Rect

prefix = "mode_indicator"
current_mode = ""
canvas: Canvas = None
mod = Module()

setting_show = mod.setting(
    f"{prefix}_show",
    bool,
    default=False,
)
setting_color_sleep = mod.setting(
    f"{prefix}_color_sleep",
    str,
    default="808080",  # Grey
)
setting_color_dictation = mod.setting(
    f"{prefix}_color_dictation",
    str,
    default="da70d6",  # Orchid
)
setting_color_mixed = mod.setting(
    f"{prefix}_color_mixed",
    str,
    default="6b8e23",  # OliveDrab
)
setting_color_other = mod.setting(
    f"{prefix}_color_other",
    str,
    default="f8f8ff",  # GhostWhite
)
setting_color_alpha = mod.setting(
    f"{prefix}_color_alpha",
    str,
    default="aa",
)

setting_paths = {
    s.path
    for s in [
        setting_show,
        setting_color_sleep,
        setting_color_dictation,
        setting_color_mixed,
        setting_color_other,
        setting_color_alpha,
    ]
}


def get_color() -> str:
    if current_mode == "sleep":
        color = setting_color_sleep.get()
    elif current_mode == "dictation":
        color = setting_color_dictation.get()
    elif current_mode == "mixed":
        color = setting_color_mixed.get()
    else:
        color = setting_color_other.get()
    return color + setting_color_alpha.get()


def on_draw(c: SkiaCanvas):
    c.paint.style = c.paint.Style.FILL
    c.paint.color = get_color()
    c.paint.imagefilter = ImageFilter.drop_shadow(1, 1, 1, 1, "000000")
    radius = c.rect.height / 2 - 2
    c.draw_circle(c.rect.center.x, c.rect.top + radius, radius)


def show_indicator():
    global canvas
    screen: Screen = ui.main_screen()
    radius = screen.dpi / 10
    side = radius * 2
    rect = Rect(screen.rect.center.x - radius, screen.rect.top, side, side)
    canvas = Canvas.from_rect(rect)
    canvas.register("draw", on_draw)


def hide_indicator():
    global canvas
    canvas.unregister("draw", on_draw)
    canvas.close()
    canvas = None


def update_indicator():
    if setting_show.get():
        if not canvas:
            show_indicator()
        canvas.freeze()
    elif canvas:
        hide_indicator()


def on_update_contexts():
    global current_mode
    modes = scope.get("mode")
    if "sleep" in modes:
        mode = "sleep"
    elif "dictation" in modes:
        if "command" in modes:
            mode = "mixed"
        else:
            mode = "dictation"
    else:
        mode = "other"

    if current_mode != mode:
        current_mode = mode
        update_indicator()


def on_update_settings(updated_settings: set[str]):
    if setting_paths & updated_settings:
        update_indicator()


def on_ready():
    registry.register("update_contexts", on_update_contexts)
    registry.register("update_settings", on_update_settings)
    ui.register("screen_change", update_indicator)


app.register("ready", on_ready)
