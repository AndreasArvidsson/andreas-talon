from talon import Module, actions, imgui, ui
import logging

mod = Module()
mod.mode("history")

# list of recent phrases, most recent first
phrase_history = []
phrase_history_display_length = 30
last_unformated = ""

main_screen = ui.main_screen()


@imgui.open(x=main_screen.x, y=main_screen.y)
def gui(gui: imgui.GUI):
    gui.text("History")
    gui.line()
    for index, text in enumerate(phrase_history[:phrase_history_display_length], 1):
        index = f"{index}".ljust(2)
        if len(text) > 25:
            text = text[:25] + "..."
        gui.text(f"{index} {text}")
    gui.spacer()
    if gui.button("Clear"):
        actions.user.history_clear()
    if gui.button("Hide"):
        actions.user.history_hide()


@mod.action_class
class Actions:
    def history_get_last_phrase() -> str:
        """Gets the last phrase"""
        return phrase_history[0] if phrase_history else ""

    def history_get_last_unformatted() -> str:
        """Get last unformatted phrase"""
        return last_unformated

    def history_get_phrase(number: int) -> str:
        """Gets the nth most recent phrase"""
        try:
            return phrase_history[number-1]
        except IndexError:
            return ""

    def history_clear_last_phrase():
        """Clears the last phrase"""
        global last_unformated
        if not phrase_history:
            return
        for _ in phrase_history[0]:
            actions.edit.delete()
        phrase_history.pop(0)
        last_unformated = ""

    def history_select_last_phrase():
        """Selects the last phrase"""
        if not phrase_history:
            logging.warning(
                "history_select_last_phrase(): No last phrase to select!")
            return
        for _ in phrase_history[0]:
            actions.edit.extend_left()

    def history_add_phrase(text: str, unformatted: str = ""):
        """Adds a phrase to the phrase history"""
        global last_unformated
        if text in phrase_history:
            phrase_history.remove(text)
        phrase_history.insert(0, text)
        last_unformated = unformatted

    def history_toggle_show():
        """Toggles list of recent phrases"""
        if gui.showing:
            actions.user.history_hide()
        else:
            gui.show()
            actions.mode.enable("user.history")

    def history_hide():
        """Hide list of recent phrases"""
        actions.mode.disable("user.history")
        gui.hide()

    def history_replace_last_phrase(text: str, unformatted: str = ""):
        """Replace last phrase in hostiry list"""
        global last_unformated
        phrase_history[0] = text
        last_unformated = unformatted
        if phrase_history.count(text) > 1:
            phrase_history.reverse()
            phrase_history.remove(text)
            phrase_history.reverse()

    def history_clear():
        """Clear history"""
        global phrase_history
        phrase_history = []

    def history_remove(number: int):
        """Remove history phrase"""
        global last_unformated
        if number < 1 or number > len(phrase_history):
            return
        phrase_history.pop(number-1)
        if number - 1 == 0:
            last_unformated = ""
