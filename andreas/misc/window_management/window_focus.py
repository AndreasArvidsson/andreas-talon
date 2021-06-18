from talon import Context, Module, app, imgui, ui, fs, actions
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
# Mapping between app name and list of running pids
name_to_pids = {}
pid_to_pids = {}


def parse_name(name):
    if name.lower() in overrides:
        return overrides[name.lower()]
    if name.endswith(".exe"):
        name = name.rsplit(".", 1)[0]
    if " - " in name:
        name = name.rsplit(" - ", 1)[0]
    # Split on camel case
    parts = re.split("(?<=[a-z])(?=[A-Z])", name)
    name = " ".join(parts)
    # Split on digits
    parts = re.split("(?<=\\D)(?=\\d)", name)
    name = " ".join(parts)
    return name


def update_lists():
    global name_to_pids, pid_to_pids
    name_to_pids = {}
    pid_to_pids = {}
    running = {}
    for app in ui.apps(background=False):
        name = parse_name(app.name)
        if not name:
            continue
        running[name] = app.name
        pids = name_to_pids.get(name, [])
        pids.append(app.pid)
        pids = sorted(pids)
        name_to_pids[app.name] = pids
        pid_to_pids[app.pid] = pids
    ctx.lists["self.running_application"] = running


def update_overrides(name, flags):
    """Updates the overrides list"""
    global overrides
    overrides = {}
    if name is None or name == override_file_path:
        with open(override_file_path, "r") as f:
            for line in f:
                line = line.rstrip()
                line = line.split(",")
                if len(line) == 2:
                    overrides[line[0].lower()] = line[1].strip()

    update_lists()


def focus_app_by_name(name: str):
    pids = name_to_pids[name]
    active_pid = ui.active_app().pid

    # Focus next window on same app
    if active_pid in pids:
        cycle_windows_on_current_app(1)
    # Focus first window of new app
    else:
        focus_app_by_pid(pids[0])


def focus_app_by_pid(pid: int):
    for app in ui.apps(background=False):
        if app.pid == pid:
            app.focus()
            actions.user.focus_hide()
            return
    raise RuntimeError(f'App not running: "{pid}"')

def cycle_windows_on_current_app(diff: int):
    # Get text window pid if same application as active
    active_pid = ui.active_app().pid
    if active_pid in pid_to_pids:
        pids = pid_to_pids[active_pid]
        i = pids.index(active_pid) + diff
        if i < 0:
            i = len(pids) - 1
        elif i >= len(pids):
            i = 0
        focus_app_by_pid(pids[i])
  

@ctx.action_class("app")
class AppActionsWin:
    def window_previous():  cycle_windows_on_current_app(-1)
    def window_next():      cycle_windows_on_current_app(1)


@mod.action_class
class Actions:
    def focus_name(name: str):
        """Focus a new application by name"""
        focus_app_by_name(name)

    def focus_index(index: int):
        """Focus a new application by index"""
        names = list(ctx.lists["user.running_application"].values())
        if index < 0 or index >= len(names):
            return
        focus_app_by_name(names[index])

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
