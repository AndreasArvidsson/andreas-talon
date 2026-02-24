from typing import Callable

from skia import RoundRect
from talon import ui
from talon.canvas import Canvas, MouseEvent
from talon.screen import Screen
from talon.types import Rect

from .button import Button
from .image import Image
from .line import Line
from .props import FONT_FAMILY, FONT_SIZE, background_color, border_color, border_radius
from .spacer import Spacer
from .state import State
from .text import Text
from .utils import get_active_screen, get_screen_scale
from .widget import Widget


class GUI:
    def __init__(
        self,
        callback: Callable,
        screen: Screen | None,
        x: float | None,
        y: float | None,
    ):
        self._callback = callback
        self._screen = screen
        self._x = x
        self._y = y
        self._x_moved = None
        self._y_moved = None
        self._screen_current = None
        self._canvas = None
        self._last_mouse_pos = None
        self._widgets: list[Widget] = []
        self._buttons: dict[str, Button] = {}

    @property
    def showing(self) -> bool:
        return self._canvas is not None

    def show(self):
        # Already showing
        if self._canvas is not None:
            return

        self._screen_current = self._screen or get_active_screen()
        self._last_mouse_pos = None

        # Initializes at minimum size so to calculate and set correct size later
        self._canvas = Canvas(self._screen_current.x, self._screen_current.y, 1, 1)
        self._canvas.draggable = True
        self._canvas.blocks_mouse = True
        self._canvas.register("draw", self._draw)
        self._canvas.register("mouse", self._mouse)

    def move(
        self,
        screen: Screen | None = None,
        x: float | None = None,
        y: float | None = None,
    ):
        if screen is not None:
            self._screen = screen
        if x is not None:
            self._x = x
            self._x_moved = None
        if y is not None:
            self._y = y
            self._y_moved = None

        if self.showing:
            if self._screen is None:
                self._screen_current = get_active_screen()
            self._move(0, 0)

    def freeze(self):
        if self._canvas is not None:
            self._canvas.freeze()

    def hide(self):
        if self._canvas is not None:
            self._canvas.unregister("draw", self._draw)
            self._canvas.unregister("mouse", self._mouse)
            self._canvas.close()
            self._canvas = None
            self._buttons = {}

    def text(self, text: str):
        self._widgets.append(Text(text, header=False))

    def header(self, text: str):
        self._widgets.append(Text(text, header=True))

    def image(self, image):
        self._widgets.append(Image(image))

    def button(self, text: str, id: str | None = None) -> bool:
        key = id or text
        if key in self._buttons:
            button = self._buttons[key]
        else:
            button = Button(text)
            self._buttons[key] = button
        self._widgets.append(button)
        return button.clicked()

    def line(self, bold: bool = False):
        self._widgets.append(Line(bold))

    def spacer(self):
        self._widgets.append(Spacer())

    def _draw(self, canvas):
        # Should not happen
        if self._screen_current is None:
            return

        canvas.paint.typeface = FONT_FAMILY
        self._widgets = []
        self._callback(self)
        self._draw_background(canvas)
        font_size = FONT_SIZE * get_screen_scale(self._screen_current)
        state = State(self._screen_current, canvas, font_size)

        if self._widgets:
            for el in self._widgets:
                el.draw(state)
        else:
            state.width = 1
            state.height = 1

        # Resize to fit content
        if canvas.width != state.get_width() or canvas.height != state.get_height():
            self._resize(self._screen_current, state.get_width(), state.get_height())

    def _resize(self, screen: Screen, width: int, height: int):
        # Should not happen
        if self._canvas is None:
            return
        if self._x_moved is not None:
            x = self._x_moved
        elif self._x is not None:
            x = screen.x + screen.width * self._x
        else:
            x = screen.x + max(0, (screen.width - width) / 2)
        if self._y_moved is not None:
            y = self._y_moved
        elif self._y is not None:
            y = screen.y + screen.height * self._y
        else:
            y = screen.y + max(0, (screen.height - height) / 2)
        self._canvas.rect = Rect(x, y, width, height)

    def _move(self, dx: float, dy: float):
        # Should not happen
        if self._canvas is None:
            return
        self._x_moved = self._canvas.rect.x + dx
        self._y_moved = self._canvas.rect.y + dy
        center_x = self._canvas.rect.center.x + dx
        center_y = self._canvas.rect.center.y + dy
        self._screen_current = ui.screen_containing(center_x, center_y)
        self._canvas.move(self._x_moved, self._y_moved)

    def _draw_background(self, canvas):
        rrect = RoundRect.from_rect(canvas.rect, x=border_radius, y=border_radius)

        canvas.paint.style = canvas.paint.Style.FILL
        canvas.paint.color = background_color
        canvas.draw_rrect(rrect)

        canvas.paint.style = canvas.paint.Style.STROKE
        canvas.paint.color = border_color
        canvas.draw_rrect(rrect)

    def _mouse(self, e: MouseEvent):
        if e.event == "mousedown" and e.button == 0:
            button = self._get_button(e.gpos)
            if button is None:
                self._last_mouse_pos = e.gpos

        elif e.event == "mousemove" and self._last_mouse_pos:
            dx = e.gpos.x - self._last_mouse_pos.x
            dy = e.gpos.y - self._last_mouse_pos.y
            self._last_mouse_pos = e.gpos
            self._move(dx, dy)

        elif e.event == "mouseup" and e.button == 0:
            self._last_mouse_pos = None
            button = self._get_button(e.gpos)
            if button is not None:
                button.click()

    def _get_button(self, pos):
        for w in self._buttons.values():
            if w.rect is not None and w.rect.contains(pos.x, pos.y):
                # self._buttons could contain removed buttons. Check if button is still in widgets before returning.
                if w in self._widgets:
                    return w
        return None
