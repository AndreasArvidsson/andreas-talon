from talon import Context, Module, app, imgui, ui, fs, actions
from user.util import cycle, split_camel
import os
import re

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
    name = " ".join(split_camel(name))
    return name

def update_lists():
    global name_to_pids
    name_to_pids = {}
    running = {}
    for window in ui.windows():
        app_name = window.app.name
        name = parse_name(app_name)
        if not name:
            continue
        running[name] = app_name
    ctx.lists["self.running_application"] = running


def update_overrides(name, flags):
    """Updates the overrides list"""
    global overrides
    res = {}
    if name is None or name == override_file_path:
        with open(override_file_path, "r") as f:
            for line in f:
                line = line.rstrip()
                line = line.split(",")
                if len(line) == 2:
                    res[line[0].lower()] = line[1].strip()
    overrides = res
    update_lists()

def get_windows(app_name: str) -> list:
    res = filter(lambda w: w.app.name == app_name, ui.windows())
    res = sorted(res, key=lambda w: w.id)
    return list(res)

def focus_app(name: str, diff: int = 1):
    windows = get_windows(name)
    if (len(windows) == 0):
        raise RuntimeError(f'App not running: "{name}"')
    i = 0
    # Focus next window on same app
    if ui.active_app().name == name:
        i = cycle(
            windows.index(ui.active_window()) + diff,
            0,
            len(windows) -1
        )
    windows[i].focus()


@ctx.action_class("app")
class AppActionsWin:
    def window_previous():
        focus_app(ui.active_app().name, -1)
    def window_next():
        focus_app(ui.active_app().name, 1)


@mod.action_class
class Actions:
    def focus_name(name: str):
        """Focus application by name"""
        focus_app(name)
        actions.user.focus_hide()

    def focus_index(index: int):
        """Focus application by index"""
        names = list(ctx.lists["user.running_application"].values())
        if index > -1 and index < len(names):
            actions.user.focus_name(names[index])

    def focus_toggle():
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


@imgui.open(x=0)
def gui(gui: imgui.GUI):
    gui.text("Focus")
    gui.line()
    index = 1
    for name in ctx.lists["self.running_application"]:
        gui.text(f"Focus {index}: {name}")
        index += 1
    gui.line()
    if gui.button("Hide"):
        actions.user.focus_hide()


def on_launch_close(event):
    update_lists()


def on_ready():
    update_overrides(None, None)
    fs.watch(overrides_directory, update_overrides)
    ui.register("app_launch", on_launch_close)
    ui.register("app_close", on_launch_close)


app.register("ready", on_ready)
