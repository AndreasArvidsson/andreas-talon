from talon import skia, ui
from talon.skia.image import Image
from talon.skia.imagefilter import ImageFilter as ImageFilter
from talon.canvas import Canvas
from talon.screen import Screen
from typing import Callable, Optional

background_color = "fafafa"
border_color = "000000"
text_color = "444444"
outer_padding = 27
border_radius = 8
text_size = 16
text_size_header = 20
line_height = 24
padding = 4


class State:
    def __init__(self, canvas: skia.Canvas, numbered: bool):
        self.canvas = canvas
        self.x = canvas.x + padding + (round(1.5 * text_size) if numbered else 0)
        self.y = canvas.y + padding
        self.width = 0
        self.height = 0


# if len(text) > max_cols + 4:
#                 text = text[:max_cols] + " ..."


class Text:
    def __init__(self, text: str, header: bool):
        self.numbered = not header
        self.text = text
        self.header = header

    def draw(self, state: State):
        size = text_size_header if self.header else text_size
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = self.header
        state.canvas.paint.textsize = size
        state.canvas.paint.color = text_color

        lines = self.text.split("\n")
        for line in lines:
            rect = state.canvas.paint.measure_text(line)[1]
            state.canvas.draw_text(line, state.x, state.y + size)
            state.width = max(state.width, rect.width)
            height = size + 2 * padding
            state.height += height
            state.y += height

        # rect = state.canvas.paint.measure_text(self.text)[1]
        # state.canvas.draw_text(self.text, state.x, state.y + size)
        # state.width = max(state.width, rect.width)
        # height = size + 2 * padding
        # state.height += height
        # state.y += height

    @classmethod
    def draw_number(cls, canvas: skia.Canvas, y: int, number: int):
        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.font.embolden = False
        canvas.paint.textsize = text_size
        text = str(number)
        rect = canvas.paint.measure_text(text)[1]
        canvas.draw_text(text, padding, y + text_size)


class Line:
    def __init__(self):
        self.numbered = False

    def draw(self, state: State):
        y = state.y + padding
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = text_color
        state.canvas.draw_line(padding, y, state.canvas.width - padding, y)
        state.height += line_height
        state.y += line_height


class Spacer:
    def __init__(self):
        self.numbered = False

    def draw(self, state: State):
        state.height += line_height
        state.y += line_height


class Image:
    def __init__(self, image: Image):
        self.numbered = True
        self._image = image

    def _resize(self, width: int, height: int) -> Image:
        aspect_ratio = self._image.width / self._image.height
        if width < height:
            height = round(width / aspect_ratio)
        else:
            width = round(height * aspect_ratio)
        return self._image.reshape(width, height)

    def draw(self, state: State):
        image = self._resize(100, 100)
        state.canvas.draw_image(image, state.x, state.y)
        height = image.height + padding * 2
        state.height += height
        state.y += height


class GUI:
    def __init__(
        self,
        callback: Callable,
        screen: Screen,
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
        self._need_resize = True
        self._resize_job = None

    @property
    def showing(self):
        return self._showing

    def show(self):
        screen = self._get_screen()
        x = screen.x + screen.width * self._x
        y = screen.y + screen.height * self._y
        # TODO
        # self._canvas = Canvas(0, 0, 1, 1)
        self._canvas = Canvas(x, y, 500, 500)
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
        state = State(canvas, self._numbered)
        number = 1

        for el in self._elements:
            if self._numbered and el.numbered:
                Text.draw_number(canvas, state.y, number)
                number += 1
            el.draw(state)

        # Resize to fit content
        # Debounce because for some reason draw gets called multiple times in quick succession.
        # self._debounce_resize(
        #     math.ceil(self.x - canvas.x + self.w + outer_padding),
        #     math.ceil(self.max_y - canvas.y + outer_padding),
        # )

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

    # def _draw_numbers_background(self, canvas):
    #     canvas.paint.style = canvas.paint.Style.FILL
    #     canvas.paint.color = text_color
    #     x = width = 4 * padding
    #     canvas.draw_line(x, padding, x, canvas.height - padding)

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

    def _get_screen(self):
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
