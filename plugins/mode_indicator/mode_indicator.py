from talon import Module, Context, app, registry, scope, skia, ui, actions, settings
from talon.canvas import Canvas
from talon.screen import Screen
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.skia.imagefilter import ImageFilter
from talon.types import Rect, Point2d

canvas: Canvas = None
current_mode = ""
mod = Module()
ctx = Context()

mod.setting(
    "mode_indicator_show",
    bool,
    desc="If true the mode indicator is shown",
    default=False,
)

# 30pixels diameter
setting_size = 30
# Center horizontally
setting_x = 0.5
# Align top
setting_y = 0
# Slightly transparent
setting_color_alpha = 0.75
# Grey gradient
setting_color_gradient = 0.5
# Black color for when the microphone is muted (set to "None")
setting_color_mute = "000000"
# Grey color for sleep mode
setting_color_sleep = "808080"
# Gold color for dictation mode
setting_color_dictation = "ffd700"
# MediumSeaGreen color for mixed mode
setting_color_mixed = "3cb371"
# CornflowerBlue color for command mode
setting_color_command = "6495ed"
# GhostWhite color for other modes
setting_color_other = "f8f8ff"


def get_mode_color() -> str:
    if not actions.user.sound_microphone_enabled():
        return setting_color_mute
    if current_mode == "sleep":
        return setting_color_sleep
    elif current_mode == "dictation":
        return setting_color_dictation
    elif current_mode == "mixed":
        return setting_color_mixed
    elif current_mode == "command":
        return setting_color_command
    else:
        return setting_color_other


def get_alpha_color() -> str:
    return f"{int(setting_color_alpha * 255):02x}"


def get_gradient_color(color: str) -> str:
    factor = setting_color_gradient
    # hex -> rgb
    (r, g, b) = tuple(int(color[i : i + 2], 16) for i in (0, 2, 4))
    # Darken rgb
    r, g, b = int(r * factor), int(g * factor), int(b * factor)
    # rgb -> hex
    return f"{r:02x}{g:02x}{b:02x}"


def get_colors():
    color_mode = get_mode_color()
    color_gradient = get_gradient_color(color_mode)
    color_alpha = get_alpha_color()
    return f"{color_mode}{color_alpha}", f"{color_gradient}"


def on_draw(c: SkiaCanvas):
    color_mode, color_gradient = get_colors()
    x, y = c.rect.center.x, c.rect.center.y
    radius = c.rect.height / 2 - 2

    c.paint.shader = skia.Shader.radial_gradient(
        Point2d(x, y), radius, [color_mode, color_gradient]
    )

    c.paint.imagefilter = ImageFilter.drop_shadow(1, 1, 1, 1, color_gradient)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = color_mode
    c.draw_circle(x, y, radius)


def move_indicator():
    screen: Screen = ui.main_screen()
    rect = screen.rect
    scale = screen.scale if app.platform != "mac" else 1
    radius = setting_size * scale / 2

    x = rect.left + min(
        max(setting_x * rect.width - radius, 0),
        rect.width - 2 * radius,
    )

    y = rect.top + min(
        max(setting_y * rect.height - radius, 0),
        rect.height - 2 * radius,
    )

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
    if settings.get("user.mode_indicator_show"):
        if not canvas:
            show_indicator()
        move_indicator()
        canvas.freeze()
    elif canvas:
        hide_indicator()


@ctx.action_class("user")
class Actions:
    def sound_microphone_enable_event():
        update_indicator()
        actions.next()


def on_mode_change(_):
    global current_mode
    modes = scope.get("mode")
    if "sleep" in modes:
        mode = "sleep"
    elif "dictation" in modes:
        if "command" in modes:
            mode = "mixed"
        else:
            mode = "dictation"
    elif "command" in modes:
        mode = "command"
    else:
        mode = "other"

    if current_mode != mode:
        current_mode = mode
        update_indicator()


def on_update_settings(updated_settings: set[str]):
    if "user.mode_indicator_show" in updated_settings:
        update_indicator()


def on_ready():
    registry._modes.register("mode_change", on_mode_change)
    registry.register("update_settings", on_update_settings)
    ui.register("screen_change", lambda _: update_indicator)
    on_mode_change({})


app.register("ready", on_ready)
