from talon import Context, Module, app, ui, actions
from talon.grammar import Phrase
import re
from ...imgui import imgui


mod = Module()
ctx = Context()

mod.mode("focus")
mod.list("running_application", desc="All running applications")
ctx.lists["self.running_application"] = {}

# Mapping of current overrides
overrides = {}


def parse_name(name):
    if name.lower() in overrides:
        return overrides[name.lower()]
    # Remove executable file ending
    if name.endswith(".exe"):
        name = name.rsplit(".", 1)[0]
    # Remove the last `-` and everything after it
    if " - " in name:
        name = name.rsplit(" - ", 1)[0]
    # Remove numbers
    name = re.sub(r"\d", "", name)
    # Split on camel case
    name = re.sub(r"[^a-zA-Z]", " ", name)
    name = actions.user.de_camel(name)
    return name


def update_running():
    running = {}
    for app in ui.apps(background=False):
        name = parse_name(app.name)
        if name:
            running[name] = app.name
    ctx.lists["self.running_application"] = running


def update_overrides(csv_dict: dict):
    """Updates the overrides list"""
    global overrides
    overrides = {k.lower(): v for k, v in csv_dict.items()}
    update_running()

    # for i in sorted(overrides):
    #     print(f"{i}: {overrides[i]}")


def focus_name(name: str):
    app = actions.user.get_app(name)
    # Focus next window on same app
    if app == ui.active_app():
        actions.app.window_next()
    # Focus app
    else:
        actions.user.focus_app(app)
    actions.user.focus_hide()


@mod.action_class
class Actions:
    def window_focus_last():
        """Switch focus to last window"""
        actions.key("alt-tab")

    def window_focus_name(name: str, phrase: Phrase = None):
        """Focus application by name"""
        focus_name(name)

        if phrase:
            actions.sleep("300ms")
            actions.user.rephrase(phrase)

    def focus_index(index: int):
        """Focus application by index"""
        names = list(ctx.lists["user.running_application"].values())
        if index > -1 and index < len(names):
            focus_name(names[index])

    def focus_help_toggle():
        """Shows/hides all running applications"""
        if gui.showing:
            actions.user.focus_hide()
        else:
            actions.mode.enable("user.focus")
            gui.show()

    def focus_hide():
        """Hides list of running applications"""
        actions.mode.disable("user.focus")
        gui.hide()


@imgui.open(numbered=True)
def gui(gui: imgui.GUI):
    gui.header("Focus")
    gui.line(bold=True)
    for name in ctx.lists["self.running_application"]:
        gui.text(name)
    gui.spacer()
    if gui.button("Hide"):
        actions.user.focus_hide()


def on_ready():
    actions.user.watch_csv_as_dict("app_name_overrides.csv", update_overrides)
    ui.register("app_launch", lambda _: update_running())
    ui.register("app_close", lambda _: update_running())


app.register("ready", on_ready)
