from talon import Module, ui, actions
from talon.screen import Screen
from talon.canvas import Canvas, MouseEvent
from talon.skia import RoundRect
from talon.skia.canvas import Canvas as SkiaCanvas
from talon.types import Rect, Point2d
from dataclasses import dataclass
from typing import Callable
import math

TEXT_SIZE = 32
HEIGHT = TEXT_SIZE * 2
WIDTH = HEIGHT * 2.5
RADIUS = WIDTH * 1.25
CORNER_RADIUS = TEXT_SIZE / 2
VERTICAL_OFFSET = HEIGHT * 1.25
BACKGROUND_COLOR = "f8f8ff"
BORDER_COLOR = "000000"
TEXT_COLOR = "000000"

mod = Module()
canvas: Canvas = None
mouse_pos: Point2d = None
rects_options: dict[str, Rect] = {}
rects_running: dict[str, Rect] = {}


@dataclass
class Option:
    text: str
    degrees: int
    callback: Callable[[], None]


options = [
    Option("Drag", -90, lambda: mouse_click("drag")),
    Option("Control", -140, lambda: mouse_click("control")),
    Option("Right", -40, lambda: mouse_click("right")),
    Option("Back", -180, actions.user.go_back),
    Option("Forward", 0, actions.user.go_forward),
    Option("Switcher", 45, lambda: actions.key("super-tab")),
    Option("Taskmgr", 135, lambda: actions.key("ctrl-shift-escape")),
]


def mouse_click(action: str):
    actions.mouse_move(mouse_pos.x, mouse_pos.y)
    actions.sleep("50ms")
    if action == "drag":
        actions.user.mouse_drag()
    actions.user.mouse_click(action)


def add_option(c: SkiaCanvas, text: str, rect: Rect):
    rrect = RoundRect.from_rect(rect, x=CORNER_RADIUS, y=CORNER_RADIUS)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = BACKGROUND_COLOR
    c.draw_rrect(rrect)

    c.paint.style = c.paint.Style.STROKE
    c.paint.color = BORDER_COLOR
    c.draw_rrect(rrect)

    c.paint.style = c.paint.Style.FILL
    c.paint.color = TEXT_COLOR
    c.paint.textsize = TEXT_SIZE
    text_rect = c.paint.measure_text(text)[1]
    c.draw_text(
        text,
        rect.center.x + text_rect.x - text_rect.width / 2,
        rect.center.y - text_rect.y - text_rect.height / 2,
    )


def get_rect(c: SkiaCanvas, option: Option) -> Rect:
    radians = math.radians(option.degrees)
    x = c.rect.center.x + RADIUS * math.cos(radians)
    y = c.rect.center.y + RADIUS * math.sin(radians)
    return Rect(x - WIDTH / 2, y - HEIGHT / 2, WIDTH, HEIGHT)


def on_draw(c: SkiaCanvas):
    global rects_options, rects_running
    rects_options = {}
    rects_running = {}

    for option in options:
        rect = get_rect(c, option)
        rects_options[option.text] = rect
        add_option(c, option.text, rect)

    running = actions.user.get_running_applications()
    x = c.rect.left + c.rect.width / 3
    y = c.rect.center.y - (((len(running) - 1) * VERTICAL_OFFSET + HEIGHT) / 2)
    for key, value in running.items():
        rect = Rect(x, y, WIDTH, HEIGHT)
        y += VERTICAL_OFFSET
        rects_running[value] = rect
        add_option(c, key, rect)

    # c.paint.style = c.paint.Style.STROKE
    # c.draw_circle(c.rect.center.x, c.rect.center.y, RADIUS)


def on_mouse(e: MouseEvent):
    if e.event == "mouseup":
        for option in options:
            rect = rects_options[option.text]
            if rect.contains(e.gpos):
                hide()
                option.callback()
                return

        for name, rect in rects_running.items():
            if rect.contains(e.gpos):
                hide()
                actions.user.window_focus_name(name)
                return

        hide()


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


@mod.action_class
class Actions:
    def quick_pick_show():
        """Show quick pick"""
        if canvas is None:
            show()
        else:
            hide()
