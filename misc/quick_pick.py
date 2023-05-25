from talon import Module, Context, ui, speech_system, actions
from talon.screen import Screen
from talon.canvas import Canvas, MouseEvent
from talon.skia import RoundRect

# from talon.skia.typeface import Typeface
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.types import Rect, Point2d
from talon.grammar import Phrase
from dataclasses import dataclass
from typing import Callable, Optional
import math

TEXT_SIZE = 32
HEIGHT = TEXT_SIZE * 2
WIDTH = HEIGHT * 2.5
RADIUS = WIDTH * 1.25
CORNER_RADIUS = TEXT_SIZE / 2
OFFSET = HEIGHT * 0.25
SNAP_WIDTH = WIDTH * 1.5
SNAP_COLORS = [
    "cd5c5c",  #  IndianRed
    "1e90ff",  # DodgerBlue
    "556b2f",  # DarkOliveGreen
    "c0c0c0",  # Silver
    "ba55d3",  # MediumOrchid
    "fa8072",  # Salmon
]
BACKGROUND_COLOR = "fffafa"  # Snow
HOVER_COLOR = "6495ed"  # CornflowerBlue
BORDER_COLOR = "000000"  # Black
TEXT_COLOR = "000000"  # Black


@dataclass
class CircleOption:
    text: str
    degrees: int
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


@dataclass
class Option:
    text: str
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


@dataclass
class Button:
    rect: Rect
    callback: Callable[[], None]
    move_mouse: Optional[bool] = False


ctx = Context()
ctx.matches = r"""
mode: all
and mode: command
mode: all
and mode: dictation
"""


mod = Module()
canvas: Canvas = None
mouse_pos: Point2d = None
hover_rect: Rect = None
last_callback: Callable[[], None] = None
buttons: list[Button] = []


circle_options = [
    CircleOption("Drag", -90, actions.user.mouse_drag, True),
    CircleOption("Control", -140, lambda: actions.user.mouse_click("control"), True),
    CircleOption("Right", -40, lambda: actions.user.mouse_click("right"), True),
    CircleOption("Back", -170, actions.user.go_back),
    CircleOption("Forward", -10, actions.user.go_forward),
    CircleOption("Tab close", 13, actions.app.tab_close),
    CircleOption("Taskmgr", 140, lambda: actions.key("ctrl-shift-escape")),
    CircleOption("Switcher", 40, lambda: actions.key("super-tab")),
    CircleOption("Search", 90, actions.user.browser_search_selected),
]

media_options = [
    # "\u23F5""⏵"
    Option("Play", lambda: actions.key("play_pause")),
    Option("Prev", lambda: actions.key("prev")),
    Option("Next", lambda: actions.key("next")),
]

snap_positions = [
    ["left", "right"],
    ["full"],
    ["top", "bottom"],
    ["left large"],
    ["center"],
    ["right large"],
    ["top left large", "bottom left large"],
    ["top center", "bottom center"],
    ["top right large", "bottom right large"],
    ["left small", "center small", "right small"],
    ["top left", "top right", "bottom left", "bottom right"],
    [
        "top left small",
        "top center small",
        "top right small",
        "bottom left small",
        "bottom center small",
        "bottom right small",
    ],
    [],
    ["middle"],
]


def add_button(c: SkiaCanvas, text: str, rect: Rect):
    rrect = RoundRect.from_rect(rect, x=CORNER_RADIUS, y=CORNER_RADIUS)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = HOVER_COLOR if hover_rect == rect else BACKGROUND_COLOR
    c.draw_rrect(rrect)

    if hover_rect == rect:
        print(text)

    c.paint.style = c.paint.Style.STROKE
    c.paint.color = BORDER_COLOR
    c.draw_rrect(rrect)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = TEXT_COLOR
    c.paint.textsize = TEXT_SIZE

    # c.paint.typeface = Typeface.from_name("Arial")
    if len(text) > 10:
        text = text[:10]

    text_rect = c.paint.measure_text(text)[1]
    c.draw_text(
        text,
        rect.center.x + text_rect.x - text_rect.width / 2,
        rect.center.y - text_rect.y - text_rect.height / 2,
    )


def draw_horizontal(c: SkiaCanvas, options: list[Option], x: float, y: float):
    x = x - ((len(options) - 1) * (WIDTH + OFFSET) + WIDTH) / 2
    for option in options:
        rect = Rect(x, y, WIDTH, HEIGHT)
        x += WIDTH + OFFSET
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_vertical(c: SkiaCanvas, options: list[Option], x: float, y: float):
    y = y - ((len(options) - 1) * (HEIGHT + OFFSET) + HEIGHT) / 2
    for option in options:
        rect = Rect(x, y, WIDTH, HEIGHT)
        y += HEIGHT + OFFSET
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_circle(c: SkiaCanvas, options: list[CircleOption], cx: float, cy: float):
    for option in options:
        radians = math.radians(option.degrees)
        x = cx + RADIUS * math.cos(radians)
        y = cy + RADIUS * 1.25 * math.sin(radians)
        rect = Rect(x - WIDTH / 2, y - HEIGHT / 2, WIDTH, HEIGHT)
        buttons.append(Button(rect, option.callback, option.move_mouse))
        add_button(c, option.text, rect)


def draw_snap_positions(c: SkiaCanvas, positions: list[list[str]], x: float, y: float):
    height = SNAP_WIDTH / (c.width / c.height)
    org_x = x - SNAP_WIDTH / 2
    x = org_x
    y = y - ((len(positions) / 3 - 1) * (height + OFFSET) + height) / 2

    for i, group in enumerate(positions):
        rect = Rect(x, y, SNAP_WIDTH, height)
        if i % 3 == 2:
            x = org_x
            y += height + OFFSET
        else:
            x += SNAP_WIDTH + OFFSET

        if len(group) == 0:
            continue

        c.paint.style = c.paint.Style.FILL
        c.paint.color = BACKGROUND_COLOR
        c.draw_rect(rect)

        for j, position in enumerate(group):
            pos_rect = actions.user.snap_apply_position_to_rect(rect, position)
            callback = (
                lambda position=position: actions.user.snap_active_window_to_position(
                    position
                )
            )
            buttons.append(Button(pos_rect, callback))
            c.paint.color = BORDER_COLOR if hover_rect == pos_rect else SNAP_COLORS[j]
            c.draw_rect(pos_rect)

        c.paint.style = c.paint.Style.STROKE
        c.paint.color = BORDER_COLOR
        c.draw_rect(rect)


def get_running_options() -> list[Option]:
    running = actions.user.get_running_applications()
    return [
        Option(key, lambda key=key: actions.user.window_focus_name(running[key]))
        for key in sorted(running)
    ]


def on_draw(c: SkiaCanvas):
    global buttons
    buttons = []

    draw_circle(
        c,
        circle_options,
        c.rect.center.x,
        c.rect.center.y,
    )

    draw_vertical(
        c,
        get_running_options(),
        c.rect.left + c.rect.width / 3,
        c.rect.center.y,
    )

    draw_horizontal(
        c,
        media_options,
        c.rect.center.x,
        c.rect.bot - c.rect.height / 3,
    )

    draw_snap_positions(
        c,
        snap_positions,
        c.rect.right + -c.rect.width / 3,
        c.rect.center.y,
    )

    # c.paint.style = c.paint.Style.STROKE
    # c.draw_circle(c.rect.center.x, c.rect.center.y, RADIUS)


def get_button_for_position(pos: Point2d):
    for button in buttons:
        if button.rect.contains(pos):
            return button
    return None


def on_mouse(e: MouseEvent):
    global last_callback, hover_rect
    button = get_button_for_position(e.gpos)

    if e.event == "mousemove":
        hover_rect_new = button.rect if button else None
        if hover_rect != hover_rect_new:
            hover_rect = hover_rect_new
            canvas.freeze()

    elif e.event == "mouseup":
        hide()
        if button:
            if button.move_mouse:
                actions.mouse_move(mouse_pos.x, mouse_pos.y)
            actions.sleep("75ms")
            button.callback()
            last_callback = button.callback


def show():
    global canvas, mouse_pos
    mouse_pos = Point2d(actions.mouse_x(), actions.mouse_y())
    screen: Screen = ui.main_screen()
    canvas = Canvas.from_screen(screen)
    canvas.blocks_mouse = True
    canvas.register("draw", on_draw)
    canvas.register("mouse", on_mouse)
    canvas.freeze()


def hide():
    global canvas
    canvas.unregister("draw", on_draw)
    canvas.unregister("mouse", on_mouse)
    canvas.close()
    canvas = None


@ctx.action_class("user")
class UserActions:
    def noise_cluck():
        if last_callback is not None:
            last_callback()
        else:
            actions.next()


@mod.action_class
class Actions:
    def quick_pick_show():
        """Show quick pick"""
        if canvas is None:
            show()
        else:
            hide()


def on_post_phrase(phrase: Phrase):
    global last_callback
    if last_callback is not None and actions.speech.enabled() and phrase.get("phrase"):
        last_callback = None


speech_system.register("post:phrase", on_post_phrase)
