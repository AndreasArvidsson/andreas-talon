from talon import app, registry, scope, ui, Module
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from talon.screen import Screen
from talon.ui import Rect

prefix = "mode_indicator"
canvas: Canvas = None
current_mode = ""
mod = Module()

setting_show = mod.setting(
    f"{prefix}_show",
    bool,
    default=False,
)
setting_radius = mod.setting(
    f"{prefix}_radius",
    float,
    default=None,
)
setting_x = mod.setting(
    f"{prefix}_x",
    float,
    default=None,
)
setting_y = mod.setting(
    f"{prefix}_y",
    float,
    default=None,
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
        setting_radius,
        setting_x,
        setting_y,
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
    c.draw_circle(c.rect.center.x, c.rect.center.y, c.rect.height / 2 - 2)


def move_indicator():
    screen: Screen = ui.main_screen()
    rect = screen.rect

    if setting_radius.get() is not None:
        radius = setting_radius.get() * screen.dpi
    else:
        radius = 0.1 * screen.dpi

    if setting_x.get() is not None:
        x = setting_x.get() * rect.width - radius
    else:
        x = rect.center.x - radius

    if setting_y.get() is not None:
        y = setting_y.get() * rect.height - radius
    else:
        y = rect.top

    side = 2 * radius
    canvas.move(x, y)
    canvas.resize(side, side)


def show_indicator():
    global canvas
    canvas = Canvas.from_rect(Rect(0, 0, 0, 0))
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
        move_indicator()
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
    ui.register("screen_change", lambda _: update_indicator)


app.register("ready", on_ready)
