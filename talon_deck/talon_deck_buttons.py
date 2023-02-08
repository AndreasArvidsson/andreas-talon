from talon import Context, actions, scope, app, cron

current_microphone = None
current_eye_tracker = None

ctx = Context()

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

ctx_game = Context()
ctx_game.matches = r"""
mode: user.game
and not mode: sleep
"""

ctx_game_listening = Context()
ctx_game_listening.matches = r"""
mode: user.game
and not mode: sleep
and not mode: user.discord_muted
"""

ctx_vscode = Context()
ctx_vscode.matches = r"""
mode: command
mode: dictation
app: vscode
"""


@ctx.action_class("user")
class Actions:
    def talon_deck_get_buttons():
        return [
            *get_microphone_buttons(),
            *get_eye_tracking_buttons(),
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
            {"icon": "gameMode", "order": 0},
        ]


@ctx_game_listening.action_class("user")
class GameListeningActions:
    def talon_deck_get_buttons():
        return [
            *actions.next(),
            {"icon": "listening", "order": 1},
        ]


@ctx_vscode.action_class("user")
class VscodeActions:
    def talon_deck_get_buttons() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "vscode"},
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
        return [{"icon": code_language}]
    return []


def get_eye_tracking_buttons():
    if current_eye_tracker:
        return [{"icon": "eyeTracking"}]
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
    active_eye_tracker = actions.user.tracking_enabled()
    if active_eye_tracker != current_eye_tracker:
        current_eye_tracker = active_eye_tracker
        actions.user.talon_deck_update()


def run_poll():
    poll_microphone()
    poll_eye_tracker()


# Use poll for features that are not updating the context
app.register("ready", lambda: cron.interval("100ms", run_poll))
