from talon import Module, ui, settings
from dataclasses import dataclass
import time
from ... import imgui
from ..analyze_phrase.types import AnalyzedPhrase

mod = Module()
history = []
mod.setting("command_history_size", int, default=25)

# If greater then zero ttl(time to live) is used to auto hide older history entries
ttl_setting = 0


# Wrapping in a data class is a simple solution to get a unique identifier for each string even if they are identical
@dataclass
class HistoryEntry:
    phrase: str
    actions: list
    ttl: int
    phrase_start: bool


@imgui.open(x=ui.main_screen().x, y=ui.main_screen().y)
def gui(gui: imgui.GUI):
    t = time.monotonic()
    use_ttl = ttl_setting > 0
    add_line = False
    # Hide entries outside of display size
    for entry in history:
        # If ttl is disabled or time hasn't passed yet: show command.
        if not use_ttl or entry.ttl < 0 or entry.ttl >= t:
            if add_line and entry.phrase_start:
                gui.line()
            add_line = True
            gui.header(entry.phrase)
            for action in entry.actions:
                gui.text(f"  {action.explanation}")


def command_history_append(analyzed_phrase: AnalyzedPhrase):
    """Append command to history"""
    global history
    ttl = time.monotonic() + ttl_setting
    for i, cmd in enumerate(analyzed_phrase.commands):
        history.append(HistoryEntry(cmd.phrase, cmd.actions, ttl, i == 0))
    size = settings.get("user.command_history_size")
    history = history[-size:]


@mod.action_class
class Actions:
    def command_history_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def command_history_clear():
        """Clear the history"""
        global history
        history = []
