from talon import Module, actions, imgui, ui
import logging

mod = Module()
mod.mode("history")

# list of recent phrases, most recent first
phrase_history = []
phrase_history_display_length = 30

main_screen = ui.main_screen()

@imgui.open(x=0, y=main_screen.y + 200)
def gui(gui: imgui.GUI):
    gui.text("History")
    gui.line()
    for index, text in enumerate(phrase_history[:phrase_history_display_length], 1):
        index = f"{index}".ljust(2)
        if len(text) > 25:
            text = text[:25] + "..."
        gui.text(f"{index} {text}")
    gui.line()
    if gui.button("Clear"):
        actions.user.history_clear()
    if gui.button("Hide"):
        actions.user.history_hide()

@mod.action_class
class Actions:
    def history_get_last_phrase() -> str:
        """Gets the last phrase"""
        return phrase_history[0] if phrase_history else ""

    def history_get_phrase(number: int) -> str:
        """Gets the nth most recent phrase"""
        try: return phrase_history[number-1]
        except IndexError: return ""

    def history_clear_last_phrase():
        """Clears the last phrase"""
        # Currently, this removes the cleared phrase from the phrase history, so
        # that repeated calls clear successively earlier phrases, which is often
        # useful. But it would be nice if we could do this without removing
        # those phrases from the history entirely, so that they were still
        # accessible for copying, for example.
        if not phrase_history:
            logging.warning("history_clear_last_phrase(): No last phrase to clear!")
            return
        for _ in phrase_history[0]:
            actions.edit.delete()
        phrase_history.pop(0)

    def history_select_last_phrase():
        """Selects the last phrase"""
        if not phrase_history:
            logging.warning("history_select_last_phrase(): No last phrase to select!")
            return
        for _ in phrase_history[0]:
            actions.edit.extend_left()

    def history_add_phrase(text: str):
        """Adds a phrase to the phrase history"""
        if len(text) < 3:
            return
        global phrase_history
        if text in phrase_history:
            phrase_history.remove(text)
        phrase_history.insert(0, text)

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

    def history_replace_last_phrase(text: str):
        """Replace last phrase in hostiry list"""
        phrase_history[0] = text
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
        global phrase_history
        if number < 1 or number > len(phrase_history):
            error = "Alternatives index {} is out of range (1-{})".format(
                number, len(phrase_history)
            )
            app.notify(error)
            raise error

        phrase_history.pop(number-1)