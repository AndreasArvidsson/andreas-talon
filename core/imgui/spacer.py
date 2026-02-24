from .state import State
from .widget import Widget


class Spacer(Widget):
    def draw(self, state: State):
        state.add_height(state.font_size)
