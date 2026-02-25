from .constants import text_color
from .state import State
from .widget import Widget


class Text(Widget):
    def __init__(self, text: str, is_header: bool):
        self.text = text
        self.is_header = is_header

    def draw(self, state: State):
        state.canvas.paint.style = state.canvas.paint.Style.FILL
        state.canvas.paint.font.embolden = self.is_header
        state.canvas.paint.textsize = state.font_size
        state.canvas.paint.color = text_color
        lines = self.text.split("\n")
        x = state.x if self.is_header else state.x_text

        for line in lines:
            line = line.replace("\t", "    ")
            rect = state.canvas.paint.measure_text(line)[1]
            state.canvas.draw_text(line, x, state.y + state.font_size)
            state.add_width(rect.x + rect.width, offset=not self.is_header)
            state.add_height(state.font_size)

        state.add_height(state.padding)
