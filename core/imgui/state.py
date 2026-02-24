from typing import Union

from skia import Canvas as SkiaCanvas
from talon import actions
from talon.screen import Screen


class State:
    max_rows: int
    max_cols: int

    def __init__(
        self,
        screen: Screen,
        canvas: SkiaCanvas,
        font_size: float,
    ):
        self.max_rows = actions.settings.get("user.gui_max_rows")
        self.max_cols = actions.settings.get("user.gui_max_cols")
        self.screen = screen
        self.canvas = canvas
        self.font_size = font_size
        self.padding = self.rem(0.5)
        self.image_height = self.max_rows * self.font_size
        self.image_width = 5 * self.image_height
        self.text_offset = self.padding
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

    def rem(self, number: Union[int, float]):
        return round(self.font_size * number)
