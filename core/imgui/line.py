from .constants import BUTTON_BG_COLOR, TEXT_COLOR
from .state import State
from .widget import Widget


class Line(Widget):
    def __init__(self, bold: bool):
        self.bold = bold

    def draw(self, state: State):
        y = state.y + state.padding - 1

        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.color = TEXT_COLOR if self.bold else BUTTON_BG_COLOR
        state.canvas.draw_line(
            state.x,
            y,
            state.x + state.canvas.width - state.font_size,
            y,
        )

        state.add_height(state.font_size)
