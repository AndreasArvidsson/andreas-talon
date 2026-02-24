from skia import RoundRect
from talon.types import Rect

from .props import border_color, button_bg_color, button_radius, button_text_color
from .state import State
from .widget import Widget


class Button(Widget):
    def __init__(self, text: str):
        self.numbered = False
        self.text = text
        self.rect = None
        self._clicked = False

    def clicked(self):
        res = self._clicked
        self._clicked = False
        return res

    def click(self):
        self._clicked = True

    def draw(self, state: State):
        state.canvas.paint.textsize = state.font_size
        text_rect = state.canvas.paint.measure_text(self.text)[1]
        padding = state.rem(0.25)
        width = text_rect.width + 2 * padding
        height = state.font_size + 2 * padding

        self.rect = Rect(
            state.x + text_rect.x - padding,
            state.y + (height + text_rect.y - text_rect.height) / 2,
            width,
            height,
        )

        rrect = RoundRect.from_rect(self.rect, x=button_radius, y=button_radius)

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
