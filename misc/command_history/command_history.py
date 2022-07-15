from talon import Module, cron, imgui, ui
from dataclasses import dataclass

mod = Module()
size_setting = mod.setting("command_history_size", int, default=50)
display_size_setting = mod.setting("command_history_display", int, default=10)
ttl_setting = mod.setting("command_history_ttl", float, default=0)
history = []
display_size = None


# Wrapping in a data class is a simple solution to get a unique identifier for each string even if they are identical
@dataclass
class HistoryEntry:
    command: str


@imgui.open(x=ui.main_screen().x, y=ui.main_screen().y)
def gui(gui: imgui.GUI):
    for entry in history[-display_size:]:
        gui.text(entry.command)


@mod.action_class
class Actions:
    def command_history_append(command: str):
        """Append command to history"""
        global history
        entry = HistoryEntry(command)
        history.append(entry)
        history = history[-size_setting.get() :]
        ttl = ttl_setting.get()
        if ttl > 0:
            cron.after(f"{int(ttl*1000)}ms", lambda: ttl_cleanup_entry(entry))

    def command_history_toggle():
        """Toggles viewing the history"""
        global display_size
        if not display_size:
            display_size = display_size_setting.get()
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def command_history_clear():
        """Clear the history"""
        global history
        history = []

    def command_history_set_size(size: int):
        """Set command history size"""
        global display_size
        if size == 0:
            gui.hide()
        else:
            display_size = size
            if not gui.showing:
                gui.show()

    def command_history_more():
        """Show more history"""
        global display_size
        if not gui.showing:
            gui.show()
            return
        if display_size < 3:
            display_size = 3
        elif display_size < 5:
            display_size = 5
        else:
            display_size += 5

    def command_history_less():
        """Show less history"""
        global display_size
        if not gui.showing:
            return
        if display_size == 1:
            gui.hide()
        elif display_size < 4:
            display_size = 1
        elif display_size < 6:
            display_size = 3
        else:
            display_size -= 5


def ttl_cleanup_entry(entry: HistoryEntry):
    if entry in history:
        history.remove(entry)
