from talon import scope, app
from ...core.imgui import imgui


@imgui.open(x=0, y=0)
def gui(gui: imgui.GUI):
    languages = list(scope.data["main"]["language"])
    languages.sort()
    for l in languages:
        gui.text(l)


# app.register("ready", lambda: gui.show())
