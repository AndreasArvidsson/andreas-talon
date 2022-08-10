from typing import Optional
from talon import Module, Context, actions, clip
from talon.skia.image import Image
from talon.clip import MimeData
from dataclasses import dataclass
from ...imgui import imgui


@dataclass
class ClipItem:
    text: str
    mime: MimeData
    image: Optional[Image]


mod = Module()
ctx = Context()
mod.mode("clipboard_manager", "Indicates that the clipboard manager is visible")


setting_clipboard_manager_max_rows = mod.setting(
    "clipboard_manager_max_rows",
    type=int,
    default=20,
)


clip_history: list[ClipItem] = []
ignore_next: bool = False
sticky: bool = False


@imgui.open(numbered=True)
def gui(gui: imgui.GUI):
    max_rows = setting_clipboard_manager_max_rows.get()
    sticky_text = " - STICKY" if sticky else ""
    gui.header(f"Clipboard ({len(clip_history)} / {max_rows}){sticky_text}")

    for i, item in enumerate(clip_history):
        gui.line(bold=i == 0)
        if item.image:
            gui.image(item.image)
        else:
            gui.text(item.text)


@ctx.action_class("clip")
class ClipActions:
    def set_text(text: str):
        clip.set_text(text)
        actions.user.clipboard_manager_update()

    def set_image(image: Image):
        clip.set_image(image)
        actions.user.clipboard_manager_update()


@mod.action_class
class Actions:
    def clipboard_manager_toggle():
        """Toggle clipboard manager"""
        if gui.showing:
            actions.user.clipboard_manager_hide()
        else:
            actions.mode.enable("user.clipboard_manager")
            gui.show()

    def clipboard_manager_toggle_sticky():
        """Toggle if the clipboard managers should be sticky"""
        global sticky
        sticky = not sticky

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

        mime = clip.mime()

        if mime is None:
            return

        text = mime.text

        try:
            image = mime.image
        except:
            image = None

        if not text:
            if image is not None:
                text = f"Image(width={image.width}, height={image.height})"
            elif is_image(mime):
                text = f"Image(UNKNOWN)"
            else:
                text = "UNKNOWN"

        append(clip_history, ClipItem(text, mime, image))
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
            hide_if_not_sticky()

    def clipboard_manager_split(numbers: list[int]):
        """Split clipboard content on new line to add new items to clipboard manager history"""
        global clip_history
        for number in numbers:
            validate_number(number)
        new_history = []
        for i, item in reversed(list(enumerate(clip_history))):
            if i + 1 in numbers and item.text:
                for line in reversed(item.text.split("\n")):
                    line = line.strip()
                    if line:
                        append(new_history, ClipItem(line, None))
            else:
                append(new_history, item)
        clip_history = new_history
        shrink()

    def clipboard_manager_copy(numbers: list[int]):
        """Copy from clipboard manager"""
        items = get_items(numbers)

        if len(items) == 1 and items[0].mime is not None:
            clip.set_mime(items[0].mime)
        else:
            texts = [i.text for i in items]
            clip.set_text("\n".join(texts))

        move_last(items)
        hide_if_not_sticky()

    def clipboard_manager_paste(numbers: list[int], match_style: bool = False):
        """Paste from clipboard manager"""
        actions.user.clipboard_manager_copy(numbers)
        if match_style:
            actions.edit.paste_match_style()
        else:
            actions.edit.paste()


def hide_if_not_sticky():
    if not sticky:
        actions.user.clipboard_manager_hide()


def move_last(items: list[ClipItem]):
    for item in items:
        clip_history.remove(item)
        clip_history.insert(0, item)


def append(history: list[ClipItem], item: ClipItem):
    if item.text:
        # Remove duplicates
        indexes = [i for i, item2 in enumerate(history) if item.text == item2.text]
        if indexes:
            history.pop(indexes[0])
    history.insert(0, item)


def get_items(numbers: list[int]):
    items = []
    for number in numbers:
        validate_number(number)
        items.append(clip_history[number - 1])
    return items


def validate_number(number: range):
    if number < 1 or number > len(clip_history):
        error(f"Clipboard manager #{number} is out of range (1-{len(clip_history)})")


def shrink():
    global clip_history
    max_rows = setting_clipboard_manager_max_rows.get()
    if len(clip_history) > max_rows:
        clip_history = clip_history[:max_rows]


def error(msg: str):
    actions.user.notify(msg)
    raise ValueError(msg)


def is_image(mime: MimeData):
    for f in mime.formats:
        if f.startswith("image/") and len(mime[f]):
            return True
    return False
