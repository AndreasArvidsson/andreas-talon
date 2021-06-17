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

mod.list("running", desc="all running applications")
ctx.lists["user.running"] = {}

# a list of the current overrides
overrides = {}

# a list of the currently running application names
running_application_dict = {}

@mod.capture(rule="{self.running}")  # | <user.text>)")
def running_applications(m) -> str:
    "Returns a single application name"
    try:
        return m.running
    except AttributeError:
        return m.text

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
    global running_application_dict
    running_application_dict = {}
    running = {}

    for cur_app in ui.apps(background=False):
        name = cur_app.name
        name = parse_name(name)
        if not name:
            continue

        running[name] = cur_app.name
        running_application_dict[cur_app.name] = True

    lists = {
        "self.running": running
    }

    # batch update lists
    ctx.lists.update(lists)

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

def get_running_app(name: str) -> ui.App:
    """Get the first available running app with `name`."""
    # We should use the capture result directly if it's already in the list
    # of running applications. Otherwise, name is from <user.text> and we
    # can be a bit fuzzier
    if name not in running_application_dict:
        if len(name) < 3:
            raise RuntimeError(
                f'Skipped getting app: "{name}" has less than 3 chars.'
            )
        for running_name, full_application_name in ctx.lists[
            "self.running"
        ].items():
            if running_name == name or running_name.lower().startswith(
                name.lower()
            ):
                name = full_application_name
                break
    for app in ui.apps():
        if app.name == name and not app.background:
            return app
    raise RuntimeError(f'App not running: "{name}"')

@mod.action_class
class Actions:
    def focus_name(name: str):
        """Focus a new application by name"""
        app = get_running_app(name)
        app.focus()
        actions.user.focus_hide()

    def focus_index(index: int):
        """Focus a new application by index"""
        names = list(ctx.lists["user.running"].values())

        if index < 1 or index > len(names):
            error = "Focus index {} is out of range (1-{})".format(
                index, len(names)
            )
            app.notify(error)
            return

        name = names[index-1]
        actions.user.focus_name(name)

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
    for line in ctx.lists["self.running"]:
        gui.text("Focus {}: {} ".format(index, line))
        index = index + 1
    gui.line()
    if gui.button("Hide"):
        actions.user.focus_hide()


def on_launch_close(event):
    update_lists()

# Talon starts faster if you don't use the `talon.ui` module during launch
def on_ready():
    update_overrides(None, None)
    fs.watch(overrides_directory, update_overrides)
    ui.register("app_launch", on_launch_close)
    ui.register("app_close", on_launch_close)

app.register("ready", on_ready)