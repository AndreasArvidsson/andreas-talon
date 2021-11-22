from talon import imgui, Module, speech_system, actions, ui

mod = Module()
setting_size_setting = mod.setting("command_history_size", int, default=50)
display_size_setting = mod.setting("command_history_display", int, default=10)
debug_timings_setting = mod.setting("debug_timings", bool, default=False)
show_subtitles = mod.setting("subtitles_show", bool, default=True).get()
history = []
display_size = None
sleep_word = "drowse"

def on_phrase(d):
    global history
    if not actions.speech.enabled():
        return
    try:
        words = d["parsed"]._unmapped
    except:
        return
    if words:
        text = " ".join(words)
        index = text.find(sleep_word)
        if index > -1:
            text = text[:index+len(sleep_word)]
        if show_subtitles:
            actions.user.subtitle(text)
        if debug_timings_setting.get():
            print(text)
            actions.user.print_phrase_timings(d)
        history.append(text)
        history = history[-setting_size_setting.get() :]


speech_system.register("phrase", on_phrase)


@imgui.open(y=ui.main_screen().y)
def gui(gui: imgui.GUI):
    for line in history[-display_size:]:
        gui.text(line)


@mod.action_class
class Actions:
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

    def toggle_subtitles():
        """Toggle subtitles"""
        global show_subtitles
        show_subtitles = not show_subtitles
