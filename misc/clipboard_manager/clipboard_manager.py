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
        actions.user.clipboard_manager_hide()


@mod.action_class
class Actions:
    def clipboard_manager_toggle():
        """Toggle clipboard manager"""
        if gui.showing:
            actions.user.clipboard_manager_hide()
        else:
            actions.mode.enable("user.clipboard_manager")
            gui.show()

    def clipboard_manager_hide():
        """Hide clipboard manager"""
        actions.mode.disable("user.clipboard_manager")
        gui.hide()

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
            shrink()

    def clipboard_manager_ignore_next():
        """Ignore next copy for clipboard manager"""
        global ignore_next
        ignore_next = True

    def clipboard_manager_remove(numbers: list[int] = None):
        """Remove clipboard manager history"""
        global clip_history
        # Remove selected history
        if numbers:
            for number in reversed(sorted(numbers)):
                validate_number(number)
                clip_history.pop(number - 1)
        # Remove entire history
        else:
            clip_history = []
            actions.user.clipboard_manager_hide()

    def clipboard_manager_split(numbers: list[int]):
        """Split clipboard content on new line to add new items to clipboard manager history"""
        global clip_history
        for number in numbers:
            validate_number(number)
        new_history = []
        for i, text in enumerate(clip_history):
            if i + 1 in numbers:
                for line in text.split("\n"):
                    line = line.strip()
                    if line:
                        new_history.append(line)
            else:
                new_history.append(text)
        clip_history = new_history
        shrink()

    def clipboard_manager_paste(numbers: list[int]):
        """Paste from clipboard manager"""
        contents = []
        for number in numbers:
            validate_number(number)
            contents.append(clip_history[number - 1])
        text = "\n".join(contents)
        actions.user.clipboard_manager_hide()
        if text:
            actions.insert(text)


def validate_number(number: range):
    if number < 1 or number > len(clip_history):
        msg = f"Clipboard manager #{number} is out of range (1-{len(clip_history)})"
        actions.user.notify(msg)
        raise ValueError(msg)


def shrink():
    global clip_history
    if len(clip_history) > max_rows:
        clip_history = clip_history[1:]
