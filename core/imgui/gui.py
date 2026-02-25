from typing import Callable

from talon import ui
from talon.canvas import Canvas, MouseEvent
from talon.screen import Screen
from talon.skia import Canvas as SkiaCanvas
from talon.skia import Image as SkiaImage
from talon.skia import RoundRect
from talon.types import Point2d, Rect

from .button import Button
from .image import Image
from .line import Line
from .constants import (
    FONT_FAMILY,
    FONT_SIZE,
    background_color,
    border_color,
    border_radius,
)
from .spacer import Spacer
from .state import State
from .props import Props
from .text import Text
from .utils import (
    NOT_SET,
    NotSetType,
    get_active_screen,
    get_screen_scale,
)
from .widget import Widget


class GUI:
    _props: Props
    _canvas: Canvas | None
    _screen: Screen | None
    _mouse_drag_pos: Point2d | None
    _widgets: list[Widget]
    _buttons: dict[str, Button]
    _buttons_seen: set[str]

    def __init__(
        self,
        callback: Callable,
        screen: Screen | None,
        x: float | None,
        y: float | None,
        width: float | None,
        height: float | None,
    ):
        self._props = Props(
            callback=callback,
            screen=screen,
            x=x,
            y=y,
            width=width,
            height=height,
        )
        self._canvas = None
        self._screen = None
        self._mouse_drag_pos = None
        self._widgets = []
        self._buttons = {}
        self._buttons_seen = set()

    @property
    def showing(self) -> bool:
        return self._canvas is not None

    def show(self):
        # Already showing
        if self._canvas is not None:
            return

        self._screen = self._props.screen or get_active_screen()

        # Initializes at minimum size so to calculate and set correct size later
        rect = self.get_initial_rect(self._screen, 0, 0, 0, 0)
        self._canvas = Canvas.from_rect(rect)

        self._canvas.draggable = True
        self._canvas.blocks_mouse = True
        self._canvas.register("draw", self._draw)
        self._canvas.register("mouse", self._mouse)

    def hide(self):
        if self._canvas is not None:
            self._canvas.unregister("draw", self._draw)
            self._canvas.unregister("mouse", self._mouse)
            self._canvas.close()
            self._canvas = None
            self._mouse_drag_pos = None
            self._widgets = []
            self._buttons = {}
            self._buttons_seen.clear()

    def update(
        self,
        *,
        screen: Screen | None | NotSetType = NOT_SET,
        x: float | None | NotSetType = NOT_SET,
        y: float | None | NotSetType = NOT_SET,
        width: float | None | NotSetType = NOT_SET,
        height: float | None | NotSetType = NOT_SET,
    ):
        old_screen = self._screen

        if not isinstance(screen, NotSetType):
            self._props.screen = screen
            self._screen = self._props.screen or get_active_screen()
        if not isinstance(x, NotSetType):
            self._props.x = x
        if not isinstance(y, NotSetType):
            self._props.y = y
        if not isinstance(width, NotSetType):
            self._props.width = width
        if not isinstance(height, NotSetType):
            self._props.height = height

        if (
            self._canvas is not None
            and old_screen is not None
            and self._screen is not None
        ):
            self._canvas.rect = self.get_initial_rect(
                self._screen,
                (self._canvas.rect.x - old_screen.x) / old_screen.width,
                (self._canvas.rect.y - old_screen.y) / old_screen.height,
                (self._canvas.rect.width) / old_screen.width,
                (self._canvas.rect.height) / old_screen.height,
            )

    def freeze(self):
        if self._canvas is not None:
            self._canvas.freeze()

    def text(self, text: str):
        self._widgets.append(Text(text, is_header=False))

    def header(self, text: str):
        self._widgets.append(Text(text, is_header=True))

    def image(self, image: SkiaImage):
        self._widgets.append(Image(image))

    def button(self, text: str, id: str | None = None) -> bool:
        """Returns whether button was clicked since last call to button()

        Duplicate text buttons require id to be set to be treated as separate buttons.
        If id is not set, buttons with the same text will be treated as the same button and share clicked state.
        """
        key = id or text
        if key in self._buttons:
            button = self._buttons[key]
            # The text could have changed for this id.
            if id is not None:
                button.text = text
        else:
            button = Button(text)
            self._buttons[key] = button
        self._widgets.append(button)
        self._buttons_seen.add(key)
        return button.clicked()

    def line(self, bold: bool = False):
        self._widgets.append(Line(bold))

    def spacer(self):
        self._widgets.append(Spacer())

    def _draw(self, canvas: SkiaCanvas):
        # Should not happen
        if self._screen is None:
            return

        canvas.paint.typeface = FONT_FAMILY
        self._widgets = []
        self._buttons_seen.clear()
        self._props.callback(self)
        self._draw_background(canvas)
        font_size = FONT_SIZE * get_screen_scale(self._screen)
        state = State(self._screen, canvas, font_size)

        if self._widgets:
            for w in self._widgets:
                w.draw(state)
        else:
            state.width = 1
            state.height = 1

        # Remove buttons that were not drawn this call
        self._buttons = {
            k: b for k, b in self._buttons.items() if k in self._buttons_seen
        }

        # Resize to fit content
        if self._props.width is not None:
            width = self._screen.width * self._props.width
        else:
            width = state.get_width()
        if self._props.height is not None:
            height = self._screen.height * self._props.height
        else:
            height = state.get_height()

        if canvas.width != width or canvas.height != height:
            self._resize(width, height)

    def _resize(self, width: float, height: float):
        # Should not happen
        if self._canvas is None or self._screen is None:
            return

        if self._props.x is not None:
            x = self._screen.x + self._screen.width * self._props.x
        else:
            x = self._screen.x + max(0, (self._screen.width - width) / 2)
        if self._props.y is not None:
            y = self._screen.y + self._screen.height * self._props.y
        else:
            y = self._screen.y + max(0, (self._screen.height - height) / 2)

        self._canvas.rect = Rect(x, y, width, height)

    def _move(self, dx: float, dy: float):
        # Should not happen
        if self._canvas is None:
            return

        x = self._canvas.rect.x + dx
        y = self._canvas.rect.y + dy
        self._screen = self.get_containing_screen(
            self._canvas.rect.center.x + dx,
            self._canvas.rect.center.y + dy,
        )
        self._props.x = (x - self._screen.x) / self._screen.width
        self._props.y = (y - self._screen.y) / self._screen.height

        self._canvas.move(x, y)

    def _draw_background(self, canvas: SkiaCanvas):
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
            # Clicking a button
            if button is not None:
                button.click()
            # Starting mouse drag
            else:
                self._mouse_drag_pos = e.gpos

        elif e.event == "mousemove" and self._mouse_drag_pos is not None:
            dx = e.gpos.x - self._mouse_drag_pos.x
            dy = e.gpos.y - self._mouse_drag_pos.y
            self._mouse_drag_pos = e.gpos
            self._move(dx, dy)

        elif e.event == "mouseup" and e.button == 0:
            # End mouse drag
            self._mouse_drag_pos = None

    def _get_button(self, pos: Point2d) -> Button | None:
        for w in self._buttons.values():
            if w.rect is not None and w.rect.contains(pos.x, pos.y):
                return w
        return None

    def get_containing_screen(self, x: float, y: float) -> Screen:
        if self._screen is not None and self._screen.rect.contains(x, y):
            return self._screen
        return ui.screen_containing(x, y)

    def get_initial_rect(
        self,
        screen: Screen,
        default_x: float,
        default_y: float,
        default_width: float,
        default_height: float,
    ) -> Rect:
        x = self._props.x if self._props.x is not None else default_x
        y = self._props.y if self._props.y is not None else default_y
        width = self._props.width if self._props.width is not None else default_width
        height = (
            self._props.height if self._props.height is not None else default_height
        )
        return Rect(
            screen.x + screen.width * x,
            screen.y + screen.height * y,
            screen.width * width,
            screen.height * height,
        )
