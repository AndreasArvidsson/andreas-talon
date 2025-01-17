from talon import scope, app
from ...core.imgui import imgui


@imgui.open(x=0, y=0)
def gui(gui: imgui.GUI):
    languages = scope.data["main"]["language"]
    for l in languages:
        gui.text(l)


# app.register("ready", lambda: gui.show())
