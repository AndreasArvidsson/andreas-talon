from talon.types import Rect

from .props import button_text_color, text_color
from .state import State
from .widget import Widget


class Text(Widget):
    def __init__(self, text: str, clickable: bool, header: bool):
        self.numbered = not header
        self.text = text
        self.header = header
        self.rect = None
        self.clickable = clickable
        self._clicked = False

    def clicked(self):
        is_clicked = self._clicked
        self._clicked = False
        return is_clicked

    def click(self):
        self._clicked = self.clickable

    def draw(self, state: State):
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = self.header
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = text_color
        x = state.x if self.header else state.x_text
        start_x = state.x
        start_y = state.y
        width = 0
        height = 0

        lines = self.text.split("\n")
        if len(lines) > state.max_rows:
            lines = lines[: state.max_rows]
            lines[-1] = "..."

        for line in lines:
            line = line.replace("\t", "    ")
            if len(line) > state.max_cols + 4:
                line = line[: state.max_cols] + " ..."
            rect = state.canvas.paint.measure_text(line)[1]
            state.canvas.draw_text(line, x, state.y + state.font_size)
            state.add_width(rect.x + rect.width, offset=not self.header)
            state.add_height(state.font_size)
            width = max(width, rect.x + rect.width)
            height += state.font_size

        self.rect = Rect(
            start_x,
            start_y,
            width + x - start_x,
            height + state.padding / 2,
        )
        # state.canvas.draw_rect(self.rect) TODO remove

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
