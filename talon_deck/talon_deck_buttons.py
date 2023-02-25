from talon import Module, Context, actions, scope, app, cron

current_microphone = None
current_eye_tracker = None

mod = Module()
ctx = Context()

ctx_command = Context()
ctx_command.matches = """
mode: command
"""

ctx_dictation = Context()
ctx_dictation.matches = """
mode: dictation
"""

ctx_sleep = Context()
ctx_sleep.matches = """
mode: sleep
"""

ctx_game = Context()
ctx_game.matches = """
mode: user.game
and not mode: sleep
"""

ctx_game_voip_listening = Context()
ctx_game_voip_listening.matches = """
mode: user.game
and not mode: sleep
and not mode: user.game_voip_muted
"""

ctx_frozen_mouse = Context()
ctx_frozen_mouse.matches = """
tag: user.mouse_frozen
"""

ctx_vscode = Context()
ctx_vscode.matches = """
mode: command
mode: dictation
app: vscode
"""


@ctx.action_class("user")
class Actions:
    def talon_deck_get_buttons():
        return [
            *get_microphone_buttons(),
            *actions.user.talon_deck_get_eye_tracker_buttons(),
        ]


@ctx_command.action_class("user")
class CommandActions:
    def talon_deck_get_buttons():
        return [
            *actions.next(),
            {"icon": "commandMode3", "action": "user.talon_sleep()", "order": 0},
            *get_code_language_buttons(),
        ]


@ctx_dictation.action_class("user")
class DictationActions:
    def talon_deck_get_buttons():
        return [
            *actions.next(),
            {"icon": get_language(), "action": "user.command_mode()", "order": 0},
        ]


@ctx_sleep.action_class("user")
class SleepActions:
    def talon_deck_get_buttons():
        return [
            *actions.next(),
            {"icon": "sleepMode", "action": "user.talon_wake()", "order": 0},
        ]


@ctx_game.action_class("user")
class GameActions:
    def talon_deck_get_buttons():
        return [
            *actions.next(),
            {"icon": "gameMode", "action": "user.game_mode_disable()", "order": 0},
        ]


@ctx_game_voip_listening.action_class("user")
class GameVoipListeningActions:
    def talon_deck_get_buttons():
        return [
            *actions.next(),
            {"icon": "listening", "action": "user.game_toggle_mute()", "order": 1},
        ]


@ctx_frozen_mouse.action_class("user")
class FrozenMouseActions:
    def talon_deck_get_eye_tracker_buttons() -> list[dict]:
        if current_eye_tracker:
            return [{"icon": "eyeTracking2", "action": "user.mouse_freeze_toggle()"}]
        return []


@ctx_vscode.action_class("user")
class VscodeActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "vscode"},
        ]


@mod.action_class
class Actions:
    def talon_deck_get_eye_tracker_buttons() -> list[dict]:
        """Return eye tracker buttons for Talon Deck"""
        if current_eye_tracker:
            return [{"icon": "eyeTracking"}]
        return []


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
        return [{"icon": code_language}]
    return []


def get_microphone_buttons():
    if current_microphone and actions.speech.enabled():
        return []
    icon = "On" if current_microphone else "Off"
    return [
        {
            "icon": f"microphone{icon}",
            "action": f"user.sound_microphone_enable({not current_microphone})",
        }
    ]


def poll_microphone():
    global current_microphone
    active_microphone = actions.user.sound_microphone_enabled()
    if active_microphone != current_microphone:
        current_microphone = active_microphone
        actions.user.talon_deck_update()


def poll_eye_tracker():
    global current_eye_tracker
    active_eye_tracker = (
        actions.tracking.control_enabled() or actions.tracking.control_zoom_enabled()
    )
    if active_eye_tracker != current_eye_tracker:
        current_eye_tracker = active_eye_tracker
        actions.user.talon_deck_update()


def run_poll():
    poll_microphone()
    poll_eye_tracker()


# Use poll for features that are not updating the context
app.register("ready", lambda: cron.interval("100ms", run_poll))
