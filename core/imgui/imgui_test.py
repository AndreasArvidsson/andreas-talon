from . import open, GUI

from talon import imgui


@imgui.open()
def test(gui):
    gui.text("test")
    pass


# test.show()


@open()
# @open(x=0)
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
    if gui.button("some text"):
        print("Hide")
    if gui.button("some text", id="other"):
        print("other")


# gui.show()

# from talon import cron
# cron.after("2s", lambda: gui.update(x=0.1))
