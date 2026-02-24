from .state import State
from .widget import Widget


class Spacer(Widget):
    def __init__(self):
        self.numbered = False
        self.rect = None

    def draw(self, state: State):
        state.add_height(state.font_size)
