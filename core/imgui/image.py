from skia import Image as SkiaImage
from talon.types import Rect

from .props import MAX_IMAGE_HEIGHT, MAX_IMAGE_WIDTH
from .state import State
from .widget import Widget


class Image(Widget):
    def __init__(self, image: SkiaImage, clickable: bool):
        self.numbered = True
        self._imageOriginal = image
        self._image = image
        self.rect = None
        self.clickable = clickable
        self._clicked = False

    def clicked(self):
        res = self._clicked
        self._clicked = False
        return res

    def click(self):
        self._clicked = self.clickable

    def _resize(self, state: State):
        max_width = state.screen.width * MAX_IMAGE_WIDTH
        max_height = state.screen.height * MAX_IMAGE_HEIGHT
        aspect_ratio = self._imageOriginal.width / self._imageOriginal.height

        width = self._imageOriginal.width
        height = self._imageOriginal.height

        if width > max_width:
            width = max_width
            height = width / aspect_ratio

        if height > max_height:
            height = max_height
            width = height * aspect_ratio

        width = int(round(width))
        height = int(round(height))

        if width != self._image.width or height != self._image.height:
            self._image = self._imageOriginal.reshape(width, height)

    def draw(self, state: State):
        self._resize(state)

        self.rect = Rect(
            state.x_text,
            state.y,
            self._image.width,
            self._image.height,
        )

        state.canvas.draw_image(self._image, state.x_text, state.y)
        state.add_width(self._image.width, offset=True)
        state.add_height(self._image.height + state.padding)
