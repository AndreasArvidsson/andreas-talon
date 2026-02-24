from talon import Module, actions, scope
from ...core import imgui

mod = Module()

mod.setting(
    "help_scope_max_length",
    type=int,
    default=50,
)


@imgui.open(x=0)
def gui(gui: imgui.GUI):
    gui.header("Scope")
    gui.line(bold=True)
    gui.spacer()
    gui.text("Modes")
    gui.line()
    for mode in sorted(scope.get("mode")):
        gui.text(mode)
    gui.spacer()
    gui.text("Tags")
    gui.line()
    for tag in sorted(scope.get("tag")):
        gui.text(tag)
    gui.spacer()
    gui.text("Misc")
    gui.line()
    ignore = {"main", "mode", "tag"}
    keys = {*scope.data.keys(), *scope.data["main"].keys()}
    for key in sorted(keys):
        if key not in ignore:
            value = scope.get(key)
            print_value(gui, key, value, ignore)
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_scope_toggle()


def print_value(gui: imgui.GUI, path: str, value, ignore: set[str] = {}):
    if isinstance(value, dict):
        for key in value:
            if key not in ignore:
                p = f"{path}.{key}" if path else key
                print_value(gui, p, value[key])
    elif value:
        gui.text(f"{path}: {format_value(value)}")


def format_value(value):
    if isinstance(value, list) or isinstance(value, set):
        value = ", ".join(sorted(value))
    if isinstance(value, str):
        max_length = actions.settings.get("user.help_scope_max_length")
        if len(value) > max_length + 4:
            return f"{value[:max_length]} ..."
    return value


@mod.action_class
class Actions:
    def help_scope_toggle():
        """Toggle help scope gui"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()
