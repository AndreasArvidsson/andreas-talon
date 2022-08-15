from talon import Module, Context, actions, registry, cron
import tempfile
import os
import json


temp_path = os.path.join(tempfile.gettempdir(), "talonDeck.json")
mod = Module()
cron_job = None

ctx = Context()
ctx.matches = r"""
os: windows
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
    def talon_deck_get_config() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "commandMode.png"},
        ]


@ctx_vscode.action_class("user")
class VscodeActions:
    def talon_deck_get_config() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "vscode.png"},
        ]


@ctx_firefox.action_class("user")
class VscodeActions:
    def talon_deck_get_config() -> list[dict]:
        return [
            *actions.next(),
            {"icon": "firefox.png"},
        ]


@mod.action_class
class Actions:
    def talon_deck_get_config() -> list[dict]:
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
    config = actions.user.talon_deck_get_config()
    file = open(temp_path, "w+")
    file.write(json.dumps(config))
    file.close()


def on_context_update():
    global cron_job
    if cron_job:
        cron.cancel(cron_job)
    cron_job = cron.after("100ms", update_file)


# registry.register("update_contexts", on_context_update)
