from pathlib import Path

from skia import Image as SkImage
from talon import imgui

from . import GUI, open


@imgui.open()
def test(gui: imgui.GUI):
    gui.text("test")
    gui.line()
    gui.text("test2")
    gui.spacer()
    gui.text("test3 test3 test3 test3")
    s = gui.slider(0, 0.5, 1)
    if s.click_value is not None:
        print("slider clicked, value:", s.click_value)
    if gui.button("a button"):
        print("button clicked")


# test.show()

images_dir = Path(__file__).parent / "images"
img1 = SkImage.load(str(images_dir / "1.jpg"))
img2 = SkImage.load(str(images_dir / "2.png"))


# @open()
@open(x=0)
# @open(y=0)
# @open(x=0.7, y=0.3)
# @open(x=0.9, y=0.3, width=0.1)
# @open(x=0.9, y=0.3, width=0.1, height=0.3)
def gui(gui: GUI):
    gui.header("Some header")
    gui.line(bold=True)
    gui.text("text before spacer")
    gui.spacer()
    gui.text("text after spacer, jg")
    for i in range(10):
        gui.line()
        gui.text(f"stuff stuff {i}")
    gui.line()
    gui.text(
        """def draw(self, state: State):
            y = state.y + state.padding - 1
            state.canvas.paint.style = state.canvas.paint.Style.FILL
            state.canvas.paint.color = text_color if self.bold else button_bg_color
            state.canvas.draw_line(
                state.x, y, state.x + state.canvas.width - state.font_size, y
            )
            state.add_height(state.font_size)"""
    )
    gui.image(img1)
    gui.image(img2)
    if gui.button("a button"):
        print("first button clicked")
    if gui.button("a button", id="other"):
        print("second button clicked")


# gui.show()
# gui.freeze()

# from talon import cron
# cron.after("2s", lambda: gui.update(x=0.1))
