from talon import Module, Context, screen, ui, cron, actions
from talon.canvas import Canvas
from datetime import datetime
import os

screenshot_folder = os.path.expanduser(os.path.join("~", "Pictures"))

mod = Module()


@mod.action_class
class Actions:
    def screenshot(screen_number: int = None):
        """Takes a screenshot of the entire screen and saves it to the pictures folder.
        Optional screen number can be given to use screen other than main."""
        screen = get_screen(screen_number)
        screenshot_rect(screen.rect)

    def screenshot_window():
        """Takes a screenshot of the active window and saves it to the pictures folder"""
        win = ui.active_window()
        screenshot_rect(win.rect, win.app.name)

    def screenshot_selection():
        """Triggers an application is capable of taking a screenshot of a portion of the screen"""

    def screenshot_clipboard(screen_number: int = None):
        """Takes a screenshot of the entire screen and saves it to the clipboard.
        Optional screen number can be given to use screen other than main."""
        screen = get_screen(screen_number)
        clipboard_rect(screen.rect)

    def screenshot_window_clipboard():
        """Takes a screenshot of the active window and saves it to the clipboard"""
        win = ui.active_window()
        clipboard_rect(win.rect)


def screenshot_rect(rect: ui.Rect, title: str = ""):
    actions.user.clear_subtitles()
    flash_rect(rect)
    img = screen.capture_rect(rect)
    path = get_screenshot_path(title)
    img.save(path)


def clipboard_rect(rect: ui.Rect):
    actions.user.clear_subtitles()
    flash_rect(rect)
    img = screen.capture_rect(rect)
    actions.clip.set_image(img)


def get_screenshot_path(title: str = ""):
    if title:
        title = f" - {title.replace('.', '_')}"
    date = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"Screenshot {date}{title}.png"
    return os.path.join(screenshot_folder, filename)


def flash_rect(rect: ui.Rect):
    def on_draw(c):
        c.paint.style = c.paint.Style.FILL
        c.paint.color = "ffffff"
        c.draw_rect(rect)
        cron.after("150ms", canvas.close)

    canvas = Canvas.from_rect(rect)
    canvas.register("draw", on_draw)
    canvas.freeze()


def get_screen(screen_number: int = None) -> ui.Screen:
    if screen_number is None:
        return screen.main_screen()
    return actions.user.screen_get_by_number(screen_number)


ctx_win = Context()
ctx_win.matches = r"""
os: windows
"""


@ctx_win.action_class("user")
class UserActionsWin:
    def screenshot_selection():
        actions.key("super-shift-s")


ctx_linux = Context()
ctx_linux.matches = r"""
os: linux
"""


@ctx_linux.action_class("user")
class UserActionsLinux:
    def screenshot_selection():
        actions.key("shift-printscr")


ctx_mac = Context()
ctx_mac.matches = r"""
os: mac
"""


@ctx_mac.action_class("user")
class UserActionsMac:
    def screenshot_selection():
        actions.key("cmd-shift-4")
