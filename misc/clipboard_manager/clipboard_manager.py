from talon import Module, actions, ui, imgui, clip

mod = Module()
mod.mode("clipboard_manager", "Indicates that the clipboard manager is visible")

clip_history = []
max_rows = 20
max_cols = 40
ignore_next = False


@imgui.open()
def gui(gui: imgui.GUI):
    gui.text(f"Clipboard ({len(clip_history)} / {max_rows})")
    gui.line()

    for i, content in enumerate(clip_history):
        content = content.replace("\n", "\\n")
        if len(content) > max_cols + 4:
            content = content[:max_cols] + " ..."
        gui.text(f"{i+1}: {content}")

    gui.spacer()
    if gui.button("Hide"):
        actions.user.clipboard_manager_toggle()


@mod.action_class
class Actions:
    def clipboard_manager_toggle():
        """Toggle clipboard manager"""
        if gui.showing:
            actions.mode.disable("user.clipboard_manager")
            gui.hide()
        else:
            actions.mode.enable("user.clipboard_manager")
            gui.show()

    def clipboard_manager_update():
        """Read current clipboard and add to manager"""
        global clip_history, ignore_next
        if ignore_next:
            ignore_next = False
            return

        text = clip.text()
        if text:
            if text in clip_history:
                clip_history.remove(text)
            clip_history.append(text)

        if len(clip_history) > max_rows:
            clip_history = clip_history[1:]

    def clipboard_manager_ignore_next():
        """Ignore next copy for clipboard manager"""
        global ignore_next
        ignore_next = True

    def clipboard_manager_remove(numbers: list[int] = None):
        """Remove clipboard manager history"""
        global clip_history
        if numbers:
            for number in reversed(sorted(numbers)):
                validate_number(number)
                clip_history.pop(number - 1)
        else:
            clip_history = []

    def clipboard_manager_paste(numbers: list[int]):
        """Paste from clipboard manager"""
        contents = []
        for number in numbers:
            validate_number(number)
            contents.append(clip_history[number - 1])
        text = "\n".join(contents)
        if text:
            actions.insert(text)


def validate_number(number: range):
    if number < 1 or number > len(clip_history):
        msg = f"Clipboard manager #{number} is out of range (1-{len(clip_history)})"
        actions.user.notify(msg)
        raise ValueError(msg)
