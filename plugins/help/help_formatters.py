from talon import Module, actions, registry
from ...core import imgui

mod = Module()


@imgui.open()
def gui(gui: imgui.GUI):
    gui.header("Formatters")
    gui.line(bold=True)

    code_formatters = registry.lists["user.formatter_code"][-1]
    prose_formatters = registry.lists["user.formatter_prose"][-1]

    if not isinstance(code_formatters, dict) or not isinstance(prose_formatters, dict):
        raise ValueError(
            f"Expected code_formatters and prose_formatters to be dicts, got {type(code_formatters)} and {type(prose_formatters)}"
        )

    formatters = {**code_formatters, **prose_formatters}

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
