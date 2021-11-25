from talon import Module, actions, imgui, Module, registry, scope, ui

mod = Module()
mod.mode("help_active_context", "Mode for showing the active context help gui")

main_screen = ui.main_screen()


@imgui.open(x=ui.main_screen().x)
def gui(gui: imgui.GUI):
    gui.text("Modes")
    gui.line()
    for mode in scope.get("mode"):
        gui.text(mode)
    gui.text("")
    gui.text("Tags")
    gui.line()
    for tag in registry.tags:
        gui.text(tag)
    gui.text("")
    gui.text("Misc")
    gui.line()
    gui.text(f"app.name: {actions.app.name()}")
    gui.text(f"code.language: {actions.code.language()}")
    gui.text("")
    if gui.button("hide"):
        actions.user.help_active_context_toggle()


@mod.action_class
class Actions:
    def help_active_context_toggle():
        """Toggle help active context gui"""
        if gui.showing:
            actions.mode.disable("user.help_active_context")
            gui.hide()
        else:
            actions.mode.enable("user.help_active_context")
            gui.show()
