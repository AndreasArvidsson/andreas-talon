from talon import Module, skia, ui
from talon.skia.image import Image
from talon.skia.imagefilter import ImageFilter as ImageFilter
from talon.canvas import Canvas
from talon.screen import Screen
from typing import Callable, Optional

background_color = "ffffff"
border_color = "000000"
text_color = "444444"
border_radius = 8

mod = Module()

setting_max_rows = mod.setting(
    "gui_max_rows",
    type=int,
    default=5,
)
setting_max_col = mod.setting(
    "gui_max_cols",
    type=int,
    default=50,
)


class State:
    def __init__(self, canvas: skia.Canvas, dpi: float, numbered: bool):
        self.max_rows = setting_max_rows.get()
        self.max_cols = setting_max_col.get()
        self.canvas = canvas
        self.font_size = round(16 * (dpi / 130))
        self.padding = self.rem(0.5)
        self.image_height = self.max_rows * self.font_size
        self.image_width = 5 * self.image_height
        self.x = canvas.x + self.padding
        self.x_text = canvas.x + self.rem(2.25) if numbered else self.x
        self.y = canvas.y + self.padding
        self.width = 0

    def get_width(self):
        if self.width:
            return round(self.x_text + self.width + self.font_size)
        else:
            return 0

    def get_height(self):
        return round(self.y + self.padding)

    def rem(self, number: int or float):
        return round(self.font_size * number)


class Text:
    def __init__(self, text: str, header: bool):
        self.numbered = not header
        self.text = text
        self.header = header

    def draw(self, state: State):
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = self.header
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = text_color

        lines = self.text.split("\n")
        if len(lines) > state.max_rows:
            lines = lines[: state.max_rows]
            lines[-1] = "..."

        for line in lines:
            if len(line) > state.max_cols + 4:
                line = line[: state.max_cols] + " ..."
            rect = state.canvas.paint.measure_text(line)[1]
            state.canvas.draw_text(line, state.x_text, state.y + state.font_size)
            state.width = max(state.width, rect.x + rect.width)
            state.y += state.font_size
        state.y += state.padding

    @classmethod
    def draw_number(cls, state: State, number: int):
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = False
        state.canvas.paint.textsize = state.font_size
        text = str(number).rjust(2)
        rect = state.canvas.paint.measure_text(text)[1]
        state.canvas.draw_text(text, state.x, state.y + state.font_size)


class Line:
    def __init__(self):
        self.numbered = False

    def draw(self, state: State):
        y = state.y + state.padding - 1
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = text_color
        state.canvas.draw_line(
            state.x, y, state.x + state.canvas.width - state.font_size, y
        )
        state.y += state.font_size


class Spacer:
    def __init__(self):
        self.numbered = False

    def draw(self, state: State):
        state.y += state.font_size


class Image:
    def __init__(self, image: Image):
        self.numbered = True
        self._image = image

    def _resize(self, width: int, height: int) -> Image:
        aspect_ratio = self._image.width / self._image.height
        if self._image.width < self._image.height:
            height = round(width / aspect_ratio)
        else:
            width = round(height * aspect_ratio)
        return self._image.reshape(width, height)

    def draw(self, state: State):
        image = self._resize(state.image_width, state.image_height)
        state.canvas.draw_image(image, state.x_text, state.y)
        state.y += image.height + state.padding
        state.width = max(state.width, image.width)


class GUI:
    def __init__(
        self,
        callback: Callable,
        screen: Screen or None,
        x: float,
        y: float,
        numbered: bool,
    ):
        self._callback = callback
        self._screen = screen
        self._x = x
        self._y = y
        self._numbered = numbered
        self._showing = False
        self._resize_job = None
        self._screen_current = None

    @property
    def showing(self):
        return self._showing

    def show(self):
        self._screen_current = self._get_screen()
        # Initializes at minimum size so to calculate and set correct size later
        self._canvas = Canvas(
            self._screen_current.x + self._screen_current.width * self._x,
            self._screen_current.y + self._screen_current.height * self._y,
            1,
            1,
        )
        self._canvas.register("draw", self._draw)
        self._showing = True

    def freeze(self):
        self._canvas.freeze()

    def hide(self):
        self._canvas.unregister("draw", self._draw)
        self._canvas.close()
        self._showing = False

    def text(self, text: str):
        self._elements.append(Text(text, header=False))

    def header(self, text: str):
        self._elements.append(Text(text, header=True))

    def line(self):
        self._elements.append(Line())

    def spacer(self):
        self._elements.append(Spacer())

    def image(self, image):
        self._elements.append(Image(image))

    def button(self, text: str) -> bool:
        return False

    def _draw(self, canvas):
        self._elements = []
        self._callback(self)
        self._draw_background(canvas)
        state = State(canvas, self._screen_current.dpi, self._numbered)
        number = 1

        for el in self._elements:
            if self._numbered and el.numbered:
                Text.draw_number(state, number)
                number += 1
            el.draw(state)

        # Resize to fit content
        if canvas.width != state.get_width() or canvas.height != state.get_height():
            self._canvas.resize(state.get_width(), state.get_height())

    def _draw_background(self, canvas):
        rrect = skia.RoundRect.from_rect(canvas.rect, x=border_radius, y=border_radius)

        # filter = ImageFilter.drop_shadow(0, 0, 1, 1, "000000")
        # canvas.paint.imagefilter = filter

        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.color = background_color
        canvas.draw_rrect(rrect)

        # canvas.paint.imagefilter = None

        canvas.paint.style = canvas.paint.Style.STROKE
        canvas.paint.color = border_color
        canvas.draw_rrect(rrect)

    def _get_screen(self) -> Screen:
        if self._screen is not None:
            return self._screen
        try:
            return ui.active_window().screen
        except:
            return ui.main_screen()


def open(
    screen: Optional[Screen] = None,
    x: Optional[float] = 0,
    y: Optional[float] = 0,
    numbered: Optional[bool] = False,
):
    def open_inner(draw):
        return GUI(
            draw,
            numbered=numbered,
            screen=screen,
            x=x,
            y=y,
        )

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
# gui.freeze()
