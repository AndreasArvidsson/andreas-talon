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
current_microphone = ""
current_eye_tracker = None

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
            {"icon": "commandMode", "action": "user.talon_sleep()", "order": 1},
            *get_code_language_buttons(),
        ]
        return buttons


@ctx_dictation.action_class("user")
class DictationActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": get_language(), "action": "user.command_mode()", "order": 1},
        ]


@ctx_sleep.action_class("user")
class SleepActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "sleepMode", "action": "user.talon_wake()", "order": 1},
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
        return [
            get_microphone_button(),
            *get_eye_tracking_buttons(),
        ]


def get_language():
    language = scope.get("language", "en_US")
    if isinstance(language, str):
        return language
    for lang in language:
        if "_" in lang:
            return lang


def get_code_language_buttons():
    code_language = actions.user.code_language()
    if code_language:
        return [{"icon": code_language, "order": 2}]
    return []


def get_eye_tracking_buttons():
    if current_eye_tracker:
        return [{"icon": "eyeTracking"}]
    return []


def get_microphone_button():
    if current_microphone == "None":
        icon = "Off"
        microphone = "System Default"
    else:
        icon = "On"
        microphone = "None"
    return {
        "icon": f"microphone{icon}",
        "action": f"sound.set_microphone('{microphone}')",
        "order": 0,
    }


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


def poll_microphone():
    global current_microphone
    active_microphone = actions.sound.active_microphone()
    if active_microphone != current_microphone:
        current_microphone = active_microphone
        on_context_update()


def poll_eye_tracker():
    global current_eye_tracker
    active_eye_tracker = (
        actions.tracking.control_enabled() or actions.tracking.control_zoom_enabled()
    )
    if active_eye_tracker != current_eye_tracker:
        current_eye_tracker = active_eye_tracker
        on_context_update()


def run_poll():
    poll_microphone()
    poll_eye_tracker()


os.makedirs(temp_dir, exist_ok=True)
registry.register("update_contexts", on_context_update)
cron.interval("200ms", run_poll)
