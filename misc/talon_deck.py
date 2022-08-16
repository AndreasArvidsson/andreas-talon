from talon import Module, Context, actions, registry, cron, app, scope
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

ctx_command = Context()
ctx_command.matches = r"""
mode: command
"""

ctx_dictation = Context()
ctx_dictation.matches = r"""
mode: dictation
"""

ctx_sleep = Context()
ctx_sleep.matches = r"""
mode: sleep
"""

ctx_vscode = Context()
ctx_vscode.matches = r"""
mode: command
mode: dictation
app: vscode
"""


@ctx_command.action_class("user")
class CommandActions:
    def talon_deck_get_buttons() -> list[dict]:
        buttons = [
            *actions.next(),
            {"icon": "commandMode", "action": "user.talon_sleep()"},
        ]
        code_language = actions.user.code_language()
        if code_language:
            buttons.append({"icon": code_language})
        return buttons


@ctx_dictation.action_class("user")
class DictationActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "dictationMode", "action": "user.command_mode()"},
            {"icon": get_language()},
        ]


@ctx_sleep.action_class("user")
class SleepActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "sleepMode", "action": "user.talon_wake()"},
        ]


@ctx_vscode.action_class("user")
class VscodeActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "vscode"},
        ]


@mod.action_class
class Actions:
    def talon_deck_get_buttons() -> list[dict]:
        """Return configuration for Talon deck"""
        return []


def get_language():
    language = scope.get("language", "en_US")
    if isinstance(language, str):
        return language
    for lang in language:
        if "_" in lang:
            return lang


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


os.makedirs(temp_dir, exist_ok=True)
registry.register("update_contexts", on_context_update)
