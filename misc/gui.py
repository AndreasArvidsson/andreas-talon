from talon import skia, cron, ui
from talon.canvas import Canvas
from typing import Callable, Optional
import math

background_color = "fafafa"
border_color = "000000"
outer_padding = 27
border_radius = 8
text_size = 16
text_size_header = 24
padding = 4


class State:
    def __init__(self, canvas: skia.Canvas):
        self.canvas = canvas
        self.y = padding
        self.width = 0
        self.height = 0


class Text:
    def __init__(self, text: str, header: bool):
        self.text = text
        self.header = header

    def draw(self, state: State):
        x = padding
        size = text_size_header if self.header else text_size
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = self.header
        state.canvas.paint.textsize = size
        rect = state.canvas.paint.measure_text(self.text)[1]
        state.canvas.draw_text(self.text, x, state.y + rect.height)
        state.width = max(state.width, rect.width)
        height = rect.height + padding * 3
        if self.header:
            height += padding
        state.height += height
        state.y += height


class Line:
    def draw(self, state: State):
        y = state.y + padding
        state.canvas.draw_line(padding, y, state.canvas.width - padding, y)
        height = padding * 4
        state.height += height
        state.y += height

class Spacer:
    def draw(self, state: State):
        y = state.y + padding
        height = padding * 4
        state.height += height
        state.y += height

class GUI:
    def __init__(self, callback: Callable):
        self._callback = callback
        self._need_resize = True
        self._resize_job = None

    def show(self):
        # self._canvas = Canvas(0, 0, 1, 1)
        self._canvas = Canvas(0, 0, 500, 500)
        self._canvas.register("draw", self._draw)

    def hide(self):
        self._canvas.unregister("draw", self._draw)
        self._canvas.close()

    def text(self, text: str) -> Text:
        self._elements.append(Text(text, header=False))

    def header(self, text: str) -> Text:
        self._elements.append(Text(text, header=True))

    def line(self) -> Line:
        self._elements.append(Line())

    def spacer(self) -> Spacer:
        self._elements.append(Spacer())

    def _draw(self, canvas):
        self._elements = []
        self._callback(self)
        self._draw_background(canvas)
        state = State(canvas)
        for el in self._elements:
            el.draw(state)

        # Resize to fit content
        # Debounce because for some reason draw gets called multiple times in quick succession.
        # self._debounce_resize(
        #     math.ceil(self.x - canvas.x + self.w + outer_padding),
        #     math.ceil(self.max_y - canvas.y + outer_padding),
        # )

    def _draw_background(self, canvas):
        rrect = skia.RoundRect.from_rect(canvas.rect, x=border_radius, y=border_radius)
        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.color = background_color
        canvas.draw_rrect(rrect)

        canvas.paint.style = canvas.paint.Style.STROKE
        canvas.paint.color = border_color
        canvas.draw_rrect(rrect)

    # def _debounce_resize(self, width: int, height: int):
    #     cron.cancel(self.resize_job)
    #     self.resize_job = cron.after("50ms", lambda: self.resize(width, height))

    # def _resize(self, width: int, height: int):
    #     if not self._need_resize:
    #         return
    #     self._need_resize = False
    #     screen = ui.main_screen()
    #     rect = ui.Rect(
    #         screen.x + (screen.width - width) / 2,
    #         screen.y + (screen.height - height) / 2,
    #         width,
    #         height,
    #     )
    #     self._canvas.rect = rect


def open(x: float, y: float):
    print(x, y)
    def open_inner(draw):
        return GUI(draw)
    return open_inner


@open(x=0.2, y=0)
def gui(gui: GUI):
    gui.header("hello")
    gui.text("aaa")
    gui.line()
    gui.text("bbb")
    gui.spacer()
    gui.text("ccc")


# gui.show()

# cron.after("2000ms", gui.hide)