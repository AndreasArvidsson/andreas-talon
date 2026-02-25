from typing import Union

from talon.screen import Screen
from talon.skia import Canvas as SkiaCanvas


class State:
    def __init__(
        self,
        screen: Screen,
        canvas: SkiaCanvas,
        font_size: float,
    ):
        self.screen = screen
        self.canvas = canvas
        self.font_size = font_size
        self.padding = self.rem(0.5)
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
        return round(self.width + self.padding)

    def get_height(self):
        return round(self.height + self.padding)

    def rem(self, number: Union[int, float]):
        return round(self.font_size * number)
