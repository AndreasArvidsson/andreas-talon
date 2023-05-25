from talon import Module, Context, app, ui, actions
from talon.grammar import Phrase
from pathlib import Path
import re


mod = Module()
ctx = Context()

mod.list("running_application", desc="All running applications")
ctx.lists["self.running_application"] = {}

# Mapping of current overrides
overrides = {}
running = {}


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
    global running
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
    actions.user.help_running_apps_hide()


@mod.action_class
class Actions:
    def window_focus_last():
        """Switch focus to last window"""
        actions.key("alt-tab")

    def window_focus_name(name: str, phrase: Phrase = None):
        """Focus application named <name>"""
        focus_name(name)

        if phrase:
            actions.sleep("300ms")
            actions.user.rephrase(phrase)

    def focus_number(number: int):
        """Focus application number <number>"""
        names = list(ctx.lists["user.running_application"].values())
        if number > 0 and number <= len(names):
            focus_name(names[number - 1])

    def get_running_applications() -> dict[str, str]:
        """Fetch a dict of running applications"""
        return running


def on_ready():
    actions.user.watch_csv_as_dict(
        Path(__file__).parent / "app_name_overrides.csv",
        update_overrides,
    )
    ui.register("app_launch", lambda _: update_running())
    ui.register("app_close", lambda _: update_running())


app.register("ready", on_ready)
