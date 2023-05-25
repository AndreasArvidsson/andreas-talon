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


@dataclass
class Option:
    text: str
    degrees: int
    callback: Callable[[], None]


@dataclass
class Button:
    rect: Rect
    callback: Callable[[], None]


mod = Module()
canvas: Canvas = None
mouse_pos: Point2d = None
buttons: list[Button] = []


options = [
    Option("Drag", -90, lambda: mouse_click("drag")),
    Option("Control", -145, lambda: mouse_click("control")),
    Option("Right", -35, lambda: mouse_click("right")),
    Option("Back", -180, actions.user.go_back),
    Option("Forward", 0, actions.user.go_forward),
    Option("Taskmgr", 145, lambda: actions.key("ctrl-shift-escape")),
    Option("Switcher", 35, lambda: actions.key("super-tab")),
    Option("Stuff", 90, lambda: actions.key("super-tab")),
]


def mouse_click(action: str):
    actions.mouse_move(mouse_pos.x, mouse_pos.y)
    actions.sleep("50ms")
    if action == "drag":
        actions.user.mouse_drag()
    actions.user.mouse_click(action)


def add_button(c: SkiaCanvas, text: str, rect: Rect):
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
    global buttons
    buttons = []

    for option in options:
        rect = get_rect(c, option)
        buttons.append(Button(rect, option.callback))
        add_button(c, option.text, rect)

    running = actions.user.get_running_applications()
    x = c.rect.left + c.rect.width / 3
    y = c.rect.center.y - (((len(running) - 1) * VERTICAL_OFFSET + HEIGHT) / 2)
    for key in sorted(running):
        rect = Rect(x, y, WIDTH, HEIGHT)
        y += VERTICAL_OFFSET
        name = running[key]
        callback = lambda name=name: actions.user.window_focus_name(name)
        buttons.append(Button(rect, callback))
        add_button(c, key, rect)

    # c.paint.style = c.paint.Style.STROKE
    # c.draw_circle(c.rect.center.x, c.rect.center.y, RADIUS)


def on_mouse(e: MouseEvent):
    if e.event == "mouseup":
        for button in buttons:
            if button.rect.contains(e.gpos):
                hide()
                print(button.rect)
                button.callback()
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
