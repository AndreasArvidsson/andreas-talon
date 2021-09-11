from talon import imgui, Module, speech_system, actions, app

mod = Module()
setting_size_setting = mod.setting("command_history_size", int, default=50)
display_size_setting = mod.setting("command_history_display", int, default=10)
show_subtitles = mod.setting("subtitles_show", int, default=True).get()
history = []
display_size = None

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
        if show_subtitles:
            actions.user.screens_show_subtitle(text)
        history.append(text)
        history = history[-setting_size_setting.get() :]


speech_system.register("phrase", on_phrase)


@imgui.open(y=0)
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
            actions.user.command_history_toggle()
            return
        if display_size == 1:
            display_size = 3
        elif display_size == 3:
            display_size = 5
        else:
            display_size += 5
        display_size = min(display_size, setting_size_setting.get())

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

    def toggle_subtitles():
        """Toggle subtitles"""
        global show_subtitles
        show_subtitles = not show_subtitles
