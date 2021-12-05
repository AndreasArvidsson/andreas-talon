from talon import Context, Module, app, imgui, ui, fs, actions
from talon.grammar import Phrase
import os
import re
import time

# Construct at startup a list of overides for application names (similar to how homophone list is managed)
cwd = os.path.dirname(os.path.realpath(__file__))
overrides_directory = cwd
override_file_name = "app_name_overrides.csv"
override_file_path = os.path.join(overrides_directory, override_file_name)

mod = Module()
ctx = Context()

mod.mode("focus")
mod.list("running_application", desc="all running applications")
ctx.lists["self.running_application"] = {}

# Mapping of current overrides
overrides = {}


def parse_name(name):
    if name.lower() in overrides:
        return overrides[name.lower()]
    if name.endswith(".exe"):
        name = name.rsplit(".", 1)[0]
    if " - " in name:
        name = name.rsplit(" - ", 1)[0]
    name = re.sub(r"[^a-zA-Z0-9]", " ", name)
    name = actions.user.de_camel(name)
    return name


def update_running():
    running = {}
    for app in ui.apps(background=False):
        name = parse_name(app.name)
        if name:
            running[name] = app.name
    ctx.lists["self.running_application"] = running


def update_overrides(name, flags):
    """Updates the overrides list"""
    global overrides
    if name != override_file_path:
        return
    res = {}
    with open(override_file_path, "r") as f:
        for line in f:
            line = line.rsplit(",", 1)
            if len(line) == 2:
                res[line[0].lower()] = line[1].strip()
    overrides = res
    update_running()

    # for i in sorted(overrides):
    #     print(f"{i}: {overrides[i]}")


def get_app(name: str) -> ui.App:
    for app in ui.apps(background=False):
        if app.name == name:
            return app
    parsed_name = parse_name(name)
    for app in ui.apps(background=False):
        if parse_name(app.name) == parsed_name:
            return app
    raise RuntimeError(f'App not running: "{name}"')


def cycle_windows(app: ui.App, diff: int):
    active = ui.active_window()
    windows = list(
        filter(lambda w: w == active or (not w.hidden and w.title != ""), app.windows())
    )
    current = windows.index(active)
    max = len(windows) - 1
    i = actions.user.cycle(current + diff, 0, max)
    while i != current:
        try:
            actions.user.focus_window(windows[i])
            break
        except:
            i = actions.user.cycle(i + diff, 0, max)


def focus_name(name: str):
    app = get_app(name)
    # Focus next window on same app
    if app == ui.active_app():
        cycle_windows(app, 1)
    # Focus app
    else:
        actions.user.focus_app(app)


@ctx.action_class("app")
class AppActionsWin:
    def window_previous():
        cycle_windows(ui.active_app(), -1)

    def window_next():
        cycle_windows(ui.active_app(), 1)


@mod.action_class
class Actions:
    def focus_name(name: str, phrase: Phrase = None):
        """Focus application by name"""
        focus_name(name)
        actions.user.focus_hide()
        if phrase:
            actions.sleep("200ms")
            actions.user.rephrase(phrase)

    def focus_names(names: list[str], phrases: list[Phrase]):
        """Focus applications by name"""
        for n, p in zip(names, phrases):
            actions.user.focus_name(n, p)

    def focus_index(index: int):
        """Focus application by index"""
        names = list(ctx.lists["user.running_application"].values())
        if index > -1 and index < len(names):
            actions.user.focus_name(names[index])

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

    def focus_app(app: ui.App):
        """Focus app and wait until finished"""
        app.focus()
        t1 = time.monotonic()
        while ui.active_app() != app:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus app: {app.name}")
            actions.sleep("50ms")

    def focus_window(window: ui.Window):
        """Focus window and wait until finished"""
        window.focus()

        t1 = time.monotonic()
        while ui.active_window() != window:
            if time.monotonic() - t1 > 1:
                raise RuntimeError(f"Can't focus window: {window.title}")
            actions.sleep("50ms")


@imgui.open(x=ui.main_screen().x)
def gui(gui: imgui.GUI):
    gui.text("Focus")
    gui.line()
    index = 1
    for name in ctx.lists["self.running_application"]:
        gui.text(f"Focus {index}: {name}")
        index += 1
    gui.spacer()
    if gui.button("Hide"):
        actions.user.focus_hide()


def on_ready():
    update_overrides(override_file_path, None)
    fs.watch(overrides_directory, update_overrides)
    ui.register("app_launch", lambda _: update_running())
    ui.register("app_close", lambda _: update_running())


app.register("ready", on_ready)
