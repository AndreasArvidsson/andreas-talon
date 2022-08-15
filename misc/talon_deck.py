from talon import Module, Context, actions, registry, cron, app
import tempfile
import os
import json

temp_dir = os.path.join(tempfile.gettempdir(), "talonDeck")
temp_path = os.path.join(temp_dir, "config.json")
repl_path = None

mod = Module()
cron_job = None

ctx = Context()
ctx.matches = r"""
mode: command
"""

ctx_vscode = Context()
ctx_vscode.matches = r"""
mode: command
app: vscode
"""

ctx_firefox = Context()
ctx_firefox.matches = r"""
mode: command
app: firefox
"""


@ctx.action_class("user")
class CommandActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "commandMode.png"},
        ]


@ctx_vscode.action_class("user")
class VscodeActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "vscode.png"},
        ]


@ctx_firefox.action_class("user")
class VscodeActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "firefox.png"},
        ]


@mod.action_class
class Actions:
    def talon_deck_get_buttons() -> list[dict]:
        """Return configuration for Talon deck"""
        result = []

        if actions.speech.enabled():
            result.append({"icon": "talonAwake.png", "action": "user.talon_sleep()"})
        else:
            result.append({"icon": "talonSleeping.png", "action": "user.talon_wake()"})

        return result


def update_file():
    global cron_job
    cron_job = None
    buttons = actions.user.talon_deck_get_buttons()
    config = {
        "buttons": buttons,
        "repl": repl_path,
    }
    file = open(temp_path, "w+")
    file.write(json.dumps(config))
    file.close()


def on_context_update():
    global cron_job
    if cron_job:
        cron.cancel(cron_job)
    cron_job = cron.after("100ms", update_file)


def get_repl_path():
    if app.platform == "windows":
        return f'"{os.path.join(actions.path.talon_home(), ".venv","Scripts", "repl.bat")}"'
    return f'"{os.path.join(actions.path.talon_home(), "bin","repl")}"'


def on_ready():
    global repl_path
    repl_path = get_repl_path()
    os.makedirs(temp_dir, exist_ok=True)
    registry.register("update_contexts", on_context_update)


# app.register("ready", on_ready)
