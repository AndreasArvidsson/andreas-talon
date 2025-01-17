from talon import scope, app
from ...core.imgui import imgui


@imgui.open(x=0, y=0)
def gui(gui: imgui.GUI):
    gui.text(str(scope.data["main"]["language"]))
    gui.text(scope.data["speech"]["engine"])


# app.register("ready", lambda: gui.show())
