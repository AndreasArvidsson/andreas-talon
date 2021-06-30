from talon import Module, screen, ui
import os

mod = Module()


@mod.action_class
class Actions:
    def screenshot_screen():
        """Take screenshot of screen"""
        img = screen.capture_rect(screen.main_screen().rect)
        path = os.path.expanduser(os.path.join("~", "Downloads", "screenshot.png"))
        img.write_file(path)    
    
    def screenshot_window():
        """Take screenshot of window"""
        img = screen.capture_rect(ui.active_window().rect)
        path = os.path.expanduser(os.path.join("~", "Downloads", "screenshot.png"))
        img.write_file(path)
