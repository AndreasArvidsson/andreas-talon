from talon import Module, Context, actions
from ...core import imgui

mod = Module()
ctx = Context()

mod.tag("help_running_apps", "Help running applications gui is showing")


@imgui.open()
def gui(gui: imgui.GUI):
    gui.header("Running apps")
    gui.line(bold=True)
    for i, name in enumerate(actions.user.get_running_applications()):
        line = f"{i + 1}".rjust(3)
        gui.text(f"{line}    {name}")
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_running_apps_toggle()


@mod.action_class
class Actions:
    def help_running_apps_toggle():
        """Toggle running applications help gui"""
        if gui.showing:
            actions.user.help_running_apps_hide()
        else:
            ctx.tags = ["user.help_running_apps"]
            gui.show()

    def help_running_apps_hide():
        """Hide running applications help gui"""
        ctx.tags = []
        gui.hide()
