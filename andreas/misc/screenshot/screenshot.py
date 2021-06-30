from talon import Module, screen, ui, cron, app, actions, clip
from datetime import datetime
from talon.canvas import Canvas
import os

mod = Module()


@mod.action_class
class Actions:
    def screenshot_screen():
        """Take screenshot of screen"""
        screenshot_rect(screen.main_screen().rect)
    
    def screenshot_window():
        """Take screenshot of window"""
        win = ui.active_window()
        title = f"{win.app.name} | {win.title}"
        screenshot_rect(win.rect, title)

    def screenshot_selection():
        """Take screenshot of selection"""
        if app.platform == "windows":
            actions.key("super-shift-s")
        elif app.platform == "mac":
            actions.key("ctrl-shift-cmd-4")
        elif app.platform == "linux":
            actions.key("shift-printscr")

    def screenshot_screen_clipboard():
        """Take screenshot of screen and saves it to the clipboard"""
        clipboard_rect(screen.main_screen().rect)

    def screenshot_window_clipboard():
        """Take screenshot of window and saves it to the clipboard"""
        clipboard_rect(ui.active_window().rect)


def screenshot_rect(rect: ui.Rect, title: str = ""):
    flash_rect(rect)
    img = screen.capture_rect(rect)
    path = get_screenshot_path(title)
    img.write_file(path)

def clipboard_rect(rect: ui.Rect):      
    flash_rect(rect)
    img = screen.capture_rect(rect)
    clip.set_image(img)

def get_screenshot_path(title: str = ""):
    if title:
        title = f" | {title}"
    date = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    filename = f"Screenshot | {date}{title}.png"
    path = os.path.expanduser(os.path.join("~", "Pictures", filename))
    return os.path.normpath(path)

def flash_rect(rect: ui.Rect):
    def on_draw(c):
        c.paint.style = c.paint.Style.FILL
        c.paint.color = "ffffff"
        c.draw_rect(rect)
        cron.after("150ms", canvas.close)

    canvas = Canvas.from_rect(rect)
    canvas.register("draw", on_draw)
    canvas.freeze()
