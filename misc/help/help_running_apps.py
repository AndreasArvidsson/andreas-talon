from talon import Module, actions, registry
from ...imgui import imgui

mod = Module()


@imgui.open(numbered=True)
def gui(gui: imgui.GUI):
    gui.header("Running apps")
    gui.line(bold=True)
    running_apps = registry.lists["user.running_application"][0]
    for name in running_apps:
        gui.text(name)
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_running_apps_toggle()


@mod.action_class
class Actions:
    def help_running_apps_toggle():
        """Toggle running applications help gui"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()
