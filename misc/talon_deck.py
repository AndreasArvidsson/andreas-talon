from talon import Module, Context, actions, registry, cron, app
from talon_init import TALON_HOME
import tempfile
import os
import json

temp_dir = os.path.join(tempfile.gettempdir(), "talonDeck")
config_path = os.path.join(temp_dir, "config.json")
repl_path = (
    f'"{os.path.join(TALON_HOME, ".venv","Scripts", "repl.bat")}"'
    if app.platform == "windows"
    else f'"{os.path.join(TALON_HOME, "bin","repl")}"'
)

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
    config = {
        "repl": repl_path,
        "buttons": actions.user.talon_deck_get_buttons(),
    }
    file = open(config_path, "w+")
    file.write(json.dumps(config))
    file.close()


def on_context_update():
    global cron_job
    if cron_job:
        cron.cancel(cron_job)
    cron_job = cron.after("100ms", update_file)


# os.makedirs(temp_dir, exist_ok=True)
# registry.register("update_contexts", on_context_update)
