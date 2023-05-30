from talon import Module, actions, registry, cron, app
from talon_init import TALON_HOME
import tempfile
import json
from pathlib import Path

config_path = Path(tempfile.gettempdir()) / "talonDeck.json"
repl_path = (
    f'{Path(TALON_HOME) / ".venv" / "Scripts" / "repl.bat"}'
    if app.platform == "windows"
    else f'{Path(TALON_HOME) / "bin" / "repl"}'
)
cron_job = None
current_file_content = ""

mod = Module()


@mod.action_class
class Actions:
    def talon_deck_get_buttons() -> list[dict]:
        """Return buttons for Talon Deck"""
        return []

    def talon_deck_update():
        """Update Talon Deck. This will trigger a call to `talon_deck_get_buttons()`"""
        update_signal()


def update_file():
    """Update configuration file on disk"""
    global cron_job, current_file_content
    cron_job = None
    config = {
        "repl": repl_path,
        "buttons": actions.user.talon_deck_get_buttons(),
    }
    file_content = json.dumps(config)
    if file_content != current_file_content:
        with open(config_path, "w") as f:
            f.write(file_content)
            current_file_content = file_content


def update_signal():
    """Signal for Talon Deck to update"""
    global cron_job
    if cron_job:
        cron.cancel(cron_job)
    # Debounce since multiple context updates triggers rapidly.
    cron_job = cron.after("10ms", update_file)


def on_ready():
    # Listen for context updates
    registry.register("update_contexts", update_signal)
    # Send heartbeat signal
    cron.interval("1s", lambda: config_path.touch())


app.register("ready", on_ready)
