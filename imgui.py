from talon import Module, skia, ui
from talon.skia.image import Image
from talon.skia.imagefilter import ImageFilter as ImageFilter
from talon.canvas import Canvas, MouseEvent
from talon.screen import Screen
from talon.ui import Rect
from typing import Callable, Optional
from dataclasses import dataclass

background_color = "ffffff"
border_color = "000000"
text_color = "444444"
button_bg_color = "aaaaaa"
button_text_color = "000000"
border_radius = 8
button_radius = 4

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
        self.font_size = round(16 * (dpi / 150))
        self.padding = self.rem(0.5)
        self.image_height = self.max_rows * self.font_size
        self.image_width = 5 * self.image_height
        self.text_offset = self.rem(2.5) if numbered else self.padding
        self.x = canvas.x + self.padding
        self.x_text = canvas.x + self.text_offset
        self.y = canvas.y + self.padding
        self.width = 0
        self.height = self.padding

    def add_width(self, width: float, offset: bool):
        text_offset = self.text_offset if offset else self.padding
        self.width = max(self.width, text_offset + width)

    def add_height(self, height: float):
        self.y += height
        self.height += height

    def get_width(self):
        if self.width:
            return round(self.width + self.padding)
        else:
            return 0

    def get_height(self):
        return round(self.height + self.padding)

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
        x = state.x if self.header else state.x_text

        lines = self.text.split("\n")
        if len(lines) > state.max_rows:
            lines = lines[: state.max_rows]
            lines[-1] = "..."

        for line in lines:
            if len(line) > state.max_cols + 4:
                line = line[: state.max_cols] + " ..."
            rect = state.canvas.paint.measure_text(line)[1]
            state.canvas.draw_text(line, x, state.y + state.font_size)
            state.add_width(rect.x + rect.width, offset=not self.header)
            state.add_height(state.font_size)
        state.add_height(state.padding)

    @classmethod
    def draw_number(cls, state: State, y_start: float, number: int):
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = False
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = button_text_color
        text = str(number).rjust(2)
        rect = state.canvas.paint.measure_text(text)[1]
        x = state.x + rect.x
        y = (state.y + y_start + rect.y + state.font_size) / 2

        # state.canvas.paint.style = state.canvas.paint.Style.FILL
        # state.canvas.paint.color = button_bg_color
        # state.canvas.draw_rect(Rect(x, y_start, rect.x + rect.width, state.y - y_start))
        # state.canvas.paint.color = button_text_color

        state.canvas.draw_text(text, x, y)


class Button:
    def __init__(self, text: str):
        self.numbered = False
        self.text = text
        self._is_pressed = False
        self._rect = None

    def is_pressed(self):
        is_pressed = self._is_pressed
        self._is_pressed = False
        return is_pressed

    def click(self):
        self._is_pressed = True

    def in_pos(self, mouse_pos) -> bool:
        rect = self._rect
        return self._in_range(
            mouse_pos.x, rect.x, rect.x + rect.width
        ) and self._in_range(mouse_pos.y, rect.y, rect.y + rect.height)

    def draw(self, state: State):
        state.canvas.paint.textsize = state.font_size
        text_rect = state.canvas.paint.measure_text(self.text)[1]
        padding = state.rem(0.25)
        width = text_rect.width + 2 * padding
        height = state.font_size + 2 * padding

        self._rect = Rect(
            state.x + text_rect.x - padding,
            state.y + (height + text_rect.y - text_rect.height) / 2,
            width,
            height,
        )

        rrect = skia.RoundRect.from_rect(self._rect, x=button_radius, y=button_radius)

        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = button_bg_color
        state.canvas.draw_rrect(rrect)

        state.canvas.paint.style = state.canvas.paint.Style.STROKE
        state.canvas.paint.color = border_color
        state.canvas.draw_rrect(rrect)

        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = False
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = button_text_color
        state.canvas.draw_text(self.text, state.x, state.y + state.font_size)

        state.add_width(width, offset=False)
        state.add_height(height + state.padding)

    def _in_range(self, value, min, max):
        return value >= min and value <= max


class Line:
    def __init__(self, bold: bool):
        self.numbered = False
        self.bold = bold

    def draw(self, state: State):
        y = state.y + state.padding - 1
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = text_color if self.bold else button_bg_color
        state.canvas.draw_line(
            state.x, y, state.x + state.canvas.width - state.font_size, y
        )
        state.add_height(state.font_size)


class Spacer:
    def __init__(self):
        self.numbered = False

    def draw(self, state: State):
        state.add_height(state.font_size)


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
        state.add_width(image.width, offset=True)
        state.add_height(image.height + state.padding)


class GUI:
    def __init__(
        self,
        callback: Callable,
        screen: Screen or None,
        x: float or None,
        y: float or None,
        numbered: bool,
    ):
        self._callback = callback
        self._screen = screen
        self._x = x
        self._y = y
        self._numbered = numbered
        self._x_moved = None
        self._y_moved = None
        self._showing = False
        self._screen_current = None
        self._buttons: dict[str, Button] = {}

    @property
    def showing(self):
        return self._showing

    def show(self):
        self._screen_current = self._get_screen()
        # Initializes at minimum size so to calculate and set correct size later
        self._canvas = Canvas(0, 0, 1, 1)
        self._showing = True
        self._canvas.draggle = True
        self._canvas.blocks_mouse = True
        self._last_mouse_pos = None
        self._canvas.register("draw", self._draw)
        self._canvas.register("mouse", self._mouse)

    def freeze(self):
        self._canvas.freeze()

    def hide(self):
        if self._showing:
            self._canvas.unregister("draw", self._draw)
            self._canvas.unregister("mouse", self._mouse)
            self._canvas.close()
            self._buttons = {}
            self._showing = False

    def text(self, text: str):
        self._elements.append(Text(text, header=False))

    def header(self, text: str):
        self._elements.append(Text(text, header=True))

    def line(self, bold: Optional[bool] = False):
        self._elements.append(Line(bold))

    def spacer(self):
        self._elements.append(Spacer())

    def image(self, image):
        self._elements.append(Image(image))

    def button(self, text: str) -> bool:
        if text in self._buttons:
            button = self._buttons[text]
        else:
            button = Button(text)
            self._buttons[text] = button
        self._elements.append(button)
        return button.is_pressed()

    def _draw(self, canvas):
        self._elements = []
        self._callback(self)
        self._draw_background(canvas)
        state = State(canvas, self._screen_current.dpi, self._numbered)
        number = 1

        # for el in self._elements:
        #     if self._numbered and el.numbered:
        #         Text.draw_number(state, number)
        #         number += 1
        #     el.draw(state)

        for el in self._elements:
            y_start = state.y
            el.draw(state)
            if self._numbered and el.numbered:
                Text.draw_number(state, y_start, number)
                number += 1

        # Resize to fit content
        if canvas.width != state.get_width() or canvas.height != state.get_height():
            self._resize(state.get_width(), state.get_height())

    def _resize(self, width: int or float, height: int or float):
        screen = self._screen_current
        if self._x_moved:
            x = self._x_moved
        elif self._x is not None:
            x = screen.x + screen.width * self._x
        else:
            x = screen.x + (screen.width - width) / 2
        if self._y_moved:
            y = self._y_moved
        elif self._y is not None:
            y = screen.y + screen.height * self._y
        else:
            y = screen.y + (screen.height - height) / 2
        self._canvas.rect = Rect(x, y, width, height)

    def _draw_background(self, canvas):
        rrect = skia.RoundRect.from_rect(canvas.rect, x=border_radius, y=border_radius)

        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.color = background_color
        canvas.draw_rrect(rrect)

        canvas.paint.style = canvas.paint.Style.STROKE
        canvas.paint.color = border_color
        canvas.draw_rrect(rrect)

    def _mouse(self, e: MouseEvent):
        if e.event == "mousedown" and e.button == 0:
            button = self._get_button_for_pos(e.gpos)
            if button is None:
                self._last_mouse_pos = e.gpos
        elif e.event == "mousemove" and self._last_mouse_pos:
            dx = e.gpos.x - self._last_mouse_pos.x
            dy = e.gpos.y - self._last_mouse_pos.y
            self._last_mouse_pos = e.gpos
            self._x_moved = self._canvas.rect.x + dx
            self._y_moved = self._canvas.rect.y + dy
            self._canvas.move(self._x_moved, self._y_moved)
            self._dont_center = True
        elif e.event == "mouseup" and e.button == 0:
            self._last_mouse_pos = None
            button = self._get_button_for_pos(e.gpos)
            if button is not None:
                button.click()

    def _get_button_for_pos(self, pos):
        for button in self._buttons.values():
            if button.in_pos(pos):
                return button
        return None

    def _get_screen(self) -> Screen:
        if self._screen is not None:
            return self._screen
        try:
            return ui.active_window().screen
        except:
            return ui.main_screen()


@dataclass
class ImGUI:
    GUI: GUI

    @classmethod
    def open(
        cls,
        screen: Optional[Screen] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
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


imgui = ImGUI(GUI)


@imgui.open(numbered=True, x=0.7, y=0.3)
def gui(gui: imgui.GUI):
    gui.header("Some header")
    gui.line(bold=True)
    gui.text("text before spacer")
    gui.spacer()
    gui.text("text after spacer, jg")
    for i in range(10):
        gui.line()
        gui.text(f"stuff stuff {i}")
    gui.line()
    gui.text(
        """def draw(self, state: State):
            y = state.y + state.padding - 1
            state.canvas.paint.style = state.canvas.paint.Style.FILL
            state.canvas.paint.color = text_color if self.bold else button_bg_color
            state.canvas.draw_line(
                state.x, y, state.x + state.canvas.width - state.font_size, y
            )
            state.add_height(state.font_size)"""
    )

    if gui.button("some text"):
        print("Hide")


# gui.show()
