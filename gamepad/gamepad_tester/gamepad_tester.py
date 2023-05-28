from talon import Module, Context, ui
from talon.screen import Screen
from talon.canvas import Canvas
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.types import Rect

mod = Module()
ctx = Context()
canvas: Canvas = None

mod.tag("gamepad_tester", "Gamepad tester gui is showing")

buttons = {
    "dpad_up": False,
    "dpad_down": False,
    "dpad_left": False,
    "dpad_right": False,
    "north": False,
    "west": False,
    "east": False,
    "south": False,
    "south": False,
    "select": False,
    "start": False,
    "l1": False,
    "r1": False,
    "l3": False,
    "r3": False,
}

triggers = {
    "l2": 0,
    "r2": 0,
}

sticks = {
    "left": (0, 0),
    "right": (0, 0),
}

BACKGROUND_COLOR = "fffafa"  # Snow
BORDER_COLOR = "000000"  # Black
WIDTH = 900
HEIGHT = 800
CIRCLE_RADIUS = 100
BUTTON_OFFSET = CIRCLE_RADIUS / 2
BUTTON_RADIUS = BUTTON_OFFSET / 2
ROW_OFFSET = CIRCLE_RADIUS * 1.25
BUTTON_FLAT_WIDTH = BUTTON_RADIUS * 3
BUTTON_FLAT_HEIGHT = BUTTON_RADIUS
TRIGGER_HEIGHT = CIRCLE_RADIUS
BUTTON_OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def render_round_button(c: SkiaCanvas, x: float, y: float, isPressed: bool):
    c.paint.style = c.paint.Style.FILL if isPressed else c.paint.Style.STROKE
    c.draw_circle(x, y, BUTTON_RADIUS)


def render_square_button(c: SkiaCanvas, x: float, y: float, isPressed: bool):
    c.paint.style = c.paint.Style.FILL if isPressed else c.paint.Style.STROKE
    c.draw_rect(
        Rect(
            x - BUTTON_RADIUS,
            y - BUTTON_RADIUS,
            BUTTON_RADIUS * 2,
            BUTTON_RADIUS * 2,
        )
    )


def render_flat_button(c: SkiaCanvas, x: float, y: float, isPressed: bool):
    c.paint.style = c.paint.Style.FILL if isPressed else c.paint.Style.STROKE
    c.draw_rect(
        Rect(
            x - BUTTON_FLAT_WIDTH / 2,
            y - BUTTON_FLAT_HEIGHT / 2,
            BUTTON_FLAT_WIDTH,
            BUTTON_FLAT_HEIGHT,
        )
    )


def render_buttons(
    c: SkiaCanvas, x: float, y: float, useCircle: bool, buttons_ids: list[str]
):
    c.paint.style = c.paint.Style.STROKE
    c.draw_circle(x, y, CIRCLE_RADIUS)
    for i, button_id in enumerate(buttons_ids):
        (offset_x, offset_y) = BUTTON_OFFSETS[i]
        button_x = x + offset_x * BUTTON_OFFSET
        button_y = y + offset_y * BUTTON_OFFSET
        isPressed = buttons[button_id]
        if useCircle:
            render_round_button(c, button_x, button_y, isPressed)
        else:
            render_square_button(c, button_x, button_y, isPressed)


def render_trigger(c: SkiaCanvas, x: float, y: float, value: float):
    # Render button outline
    c.paint.style = c.paint.Style.STROKE
    c.draw_rect(
        Rect(
            x - BUTTON_FLAT_WIDTH / 2,
            y - TRIGGER_HEIGHT,
            BUTTON_FLAT_WIDTH,
            TRIGGER_HEIGHT,
        )
    )
    # Render button value
    c.paint.style = c.paint.Style.FILL
    height = value * TRIGGER_HEIGHT
    c.draw_rect(
        Rect(
            x - BUTTON_FLAT_WIDTH / 2,
            y - height,
            BUTTON_FLAT_WIDTH,
            height,
        )
    )
    # Render value text
    text = str(round(value * 100))
    text_rect = c.paint.measure_text(text)[1]
    c.draw_text(
        text,
        x - text_rect.x - text_rect.width / 2,
        y - TRIGGER_HEIGHT - text_rect.height,
    )


def render_stick(c: SkiaCanvas, x: float, y: float, value_x: float, value_y: float):
    c.paint.style = c.paint.Style.STROKE
    # Draw outer circle
    c.draw_circle(x, y, CIRCLE_RADIUS)
    # Draw cross
    c.draw_line(x - CIRCLE_RADIUS, y, x + CIRCLE_RADIUS, y)
    c.draw_line(x, y - CIRCLE_RADIUS, x, y + CIRCLE_RADIUS)
    dot_x = x + value_x * CIRCLE_RADIUS
    dot_y = y + value_y * CIRCLE_RADIUS
    # Draw line to dot
    c.draw_line(x, y, dot_x, dot_y)
    # Draw center dot
    c.paint.style = c.paint.Style.FILL
    c.draw_circle(dot_x, dot_y, 5)
    # Render value texts
    text = f"{round(value_x * 100)}, {round(value_y * 100)}"
    text_rect = c.paint.measure_text(text)[1]
    c.draw_text(
        text,
        x - text_rect.x - text_rect.width / 2,
        y - CIRCLE_RADIUS - text_rect.height,
    )


def on_draw(c: SkiaCanvas):
    # Render background
    c.paint.style = c.paint.Style.FILL
    c.paint.color = BACKGROUND_COLOR
    c.draw_rect(c.rect)

    c.paint.color = BORDER_COLOR
    y_center = c.rect.center.y + ROW_OFFSET * 0.75

    offset = CIRCLE_RADIUS * 2.5

    # Render trigger buttons
    y = y_center - ROW_OFFSET * 2.5
    render_trigger(c, c.rect.center.x - offset, y, triggers["l2"])
    render_trigger(c, c.rect.center.x + offset, y, triggers["r2"])

    # Render shoulder buttons
    y = y_center - ROW_OFFSET * 2.15
    render_flat_button(c, c.rect.center.x - offset, y, buttons["l1"])
    render_flat_button(c, c.rect.center.x + offset, y, buttons["r1"])

    y = y_center - ROW_OFFSET

    # Render d-pad
    render_buttons(
        c,
        c.rect.center.x - offset,
        y,
        False,
        ["dpad_up", "dpad_right", "dpad_down", "dpad_left"],
    )

    # Render compass buttons
    render_buttons(
        c,
        c.rect.center.x + offset,
        y,
        True,
        ["north", "east", "south", "west"],
    )

    # Render middle buttons
    offset = CIRCLE_RADIUS * 0.75
    y = y_center - ROW_OFFSET / 3
    render_round_button(c, c.rect.center.x - offset, y, buttons["select"])
    render_round_button(c, c.rect.center.x + offset, y, buttons["start"])

    # Render sticks
    offset = CIRCLE_RADIUS * 1.5
    y = y_center + ROW_OFFSET
    render_stick(c, c.rect.center.x - offset, y, *sticks["left"])
    render_stick(c, c.rect.center.x + offset, y, *sticks["right"])


def show():
    global canvas
    screen: Screen = ui.main_screen()
    x = screen.rect.center.x
    y = screen.rect.center.y
    canvas = Canvas.from_rect(Rect(x - WIDTH / 2, y - HEIGHT / 2, WIDTH, HEIGHT))
    canvas.register("draw", on_draw)
    ctx.tags = ["user.gamepad_tester"]


def hide():
    global canvas
    canvas.unregister("draw", on_draw)
    canvas.close()
    canvas = None
    ctx.tags = []


@mod.action_class
class Actions:
    def gamepad_tester_toggle():
        """Toggle visibility of gamepad tester gui"""
        if not canvas:
            show()
        else:
            hide()

    def gamepad_tester_button(id: str, is_pressed: bool):
        """Indicates that a gamepad button has changed state"""
        buttons[id] = is_pressed

    def gamepad_tester_trigger(id: str, value: float):
        """Indicates that a gamepad trigger has changed state"""
        triggers[id] = value

    def gamepad_tester_stick(id: str, x: float, y: float):
        """Indicates that a gamepad stick has changed state"""
        sticks[id] = (x, y)
