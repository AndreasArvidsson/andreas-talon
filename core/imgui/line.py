from .props import button_bg_color, text_color
from .state import State
from .widget import Widget


class Line(Widget):
    def __init__(self, bold: bool):
        self.numbered = False
        self.bold = bold
        self.rect = None

    def draw(self, state: State):
        y = state.y + state.padding - 1
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = text_color if self.bold else button_bg_color
        state.canvas.draw_line(
            state.x, y, state.x + state.canvas.width - state.font_size, y
        )
        state.add_height(state.font_size)
