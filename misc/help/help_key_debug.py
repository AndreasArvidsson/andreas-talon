from talon import Module, Context, actions, ctrl, settings
from ...imgui import imgui

mod = Module()

mod.tag("key_debug", "Keep track of which keys are held and not")

ctx = Context()
ctx.matches = r"""
tag: user.key_debug
"""

held = set()


@imgui.open(x=0)
def gui(gui: imgui.GUI):
    gui.header("Held keys")
    gui.line(bold=True)
    gui.spacer()
    for button in ctrl.mouse_buttons_down():
        gui.text(f"Mouse {button}")
    for key in held:
        gui.text(key)

    # gui.spacer()
    # if gui.button("Hide"):
    #     actions.user.help_key_debug_toggle()


@ctx.action_class("main")
class MainActions:
    def key(key: str):
        actions.next(key)

        for k in key.split(" "):
            if ":down" in k:
                held.add(k[:-5])
            if ":up" in k:
                k = k[:-3]
                if k in held:
                    held.remove(k)


@mod.action_class
class Actions:
    def help_key_debug_toggle():
        """Toggle help key debug gui"""
        if gui.showing:
            gui.hide()
        else:
            gui.show()
