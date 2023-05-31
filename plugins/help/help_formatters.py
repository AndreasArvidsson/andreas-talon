from talon import Module, actions, registry
from ...core.imgui import imgui

mod = Module()


@imgui.open()
def gui(gui: imgui.GUI):
    gui.header("Formatters")
    gui.line(bold=True)
    formatters = {
        **registry.lists["user.formatter_code"][0],
        **registry.lists["user.formatter_prose"][0],
    }
    for name in sorted(formatters):
        gui.text(
            f"{name.ljust(30)}{actions.user.format_text('one two three', formatters[name])}"
        )
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_formatters_toggle()


@mod.action_class
class Actions:
    def help_formatters_toggle():
        """Toggle formatters help gui"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()
