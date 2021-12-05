from talon import Module, actions, imgui, Module, registry, ui

mod = Module()
mod.mode("help_alphabet", "Mode for showing the alphabet help gui")


main_screen = ui.main_screen()


@imgui.open(x=ui.main_screen().x)
def gui(gui: imgui.GUI):
    gui.text("Alphabet")
    gui.line()
    alphabet = registry.lists["user.key_alphabet"][0]
    for key, val in alphabet.items():
        gui.text(f"{val}:  {key}")
    gui.spacer()
    if gui.button("Hide"):
        actions.user.help_alphabet_toggle()


@mod.action_class
class Actions:
    def help_alphabet_toggle():
        """Toggle help alphabet gui"""
        if gui.showing:
            actions.mode.disable("user.help_alphabet")
            gui.hide()
        else:
            actions.mode.enable("user.help_alphabet")
            gui.show()
