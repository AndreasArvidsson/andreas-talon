from talon import imgui, Module, speech_system, actions, app

mod = Module()
setting_size = mod.setting("command_history_size", int, default=50)
display_size = mod.setting("command_history_display", int, default=10).get()
history = []


def parse_phrase(word_list):
    return " ".join(word.split("\\")[0] for word in word_list)

def on_phrase(j):
    global history
    if not actions.speech.enabled():
        return
    try:
        val = parse_phrase(getattr(j["parsed"], "_unmapped", j["phrase"]))
    except:
        val = parse_phrase(j["phrase"])
    if val != "":
        history.append(val)
        history = history[-setting_size.get() :]

speech_system.register("phrase", on_phrase)


@imgui.open(y=0)
def gui(gui: imgui.GUI):
    for line in history[-display_size:]:
        gui.text(line)


@mod.action_class
class Actions:
    def command_history_toggle():
        """Toggles viewing the history"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()

    def command_history_enable():
        """Enables the history"""
        gui.show()

    def command_history_disable():
        """Disables the history"""
        gui.hide()

    def command_history_clear():
        """Clear the history"""
        global history
        history = []

    def command_history_more():
        """Show more history"""
        global display_size
        if not gui.showing:
            gui.show()
            return
        if display_size == 1:
            display_size = 3
        elif display_size == 3:
            display_size = 5
        else:
            display_size += 5
        display_size = min(display_size, setting_size.get())

    def command_history_less():
        """Show less history"""
        global display_size
        if not gui.showing:
            return
        if display_size == 1:
            gui.hide()
        elif display_size == 3:
            display_size = 1
        elif display_size == 5:
            display_size = 3
        else:
            display_size -= 5
