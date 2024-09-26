from talon import Module, ctrl, ui
from talon.screen import Screen
import win32api
import win32con

mod = Module()
screen: Screen = ui.main_screen()
screen_center = screen.rect.center
default_mouse_move = ctrl.mouse_move
mouse_speed = 0.9


def relative_mouse_move(x: int, y: int):
    dx = int((x - screen_center.x) * mouse_speed)
    dy = int((y - screen_center.y) * mouse_speed)
    print(dx, dy)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy)


@mod.action_class
class Actions:
    def game_enable_relative_mouse():
        """Enable relative mouse movement"""
        ctrl.mouse_move = relative_mouse_move

    def game_disable_relative_mouse():
        """Disable relative mouse movement"""
        ctrl.mouse_move = default_mouse_move
