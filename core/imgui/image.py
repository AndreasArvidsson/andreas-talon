from skia import Image as SkImage

from .state import State
from .widget import Widget


class Image(Widget):
    def __init__(self, image: SkImage):
        self._imageOriginal = image
        self._image = image

    def _resize(self, state: State):
        aspect_ratio = self._imageOriginal.width / self._imageOriginal.height
        width = self._imageOriginal.width
        height = self._imageOriginal.height

        max_width = 30 * state.font_size
        max_height = 10 * state.font_size

        if width > max_width:
            width = max_width
            height = width / aspect_ratio

        if height > max_height:
            height = max_height
            width = height * aspect_ratio

        width = round(width)
        height = round(height)

        if width != self._image.width or height != self._image.height:
            self._image = self._imageOriginal.reshape(width, height)

    def draw(self, state: State):
        self._resize(state)

        state.canvas.draw_image(self._image, state.x_text, state.y)
        state.add_width(self._image.width, offset=True)
        state.add_height(self._image.height + state.padding)
