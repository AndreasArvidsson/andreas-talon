from talon import Module, Context, actions

mod = Module()

mod.apps.space_marine = r"""
os: windows
and app.exe: warhammer 40000 space marine 2 - retail.exe
"""

ctx_app = Context()
ctx_app.matches = r"""
app: space_marine
"""

ctx = Context()
ctx.matches = r"""
mode: user.game
app: space_marine
"""


@ctx_app.action_class("user")
class GlobalUserActions:
    def game_mode_enable():
        actions.next()
        actions.user.mouse_control_toggle(False)
        # actions.user.game_enable_relative_mouse()

    def game_mode_disable():
        """Disable game mode"""
        actions.next()
        actions.user.mouse_control_toggle(True)
        # actions.user.game_disable_relative_mouse()


@ctx.action_class("user")
class UserActions:
    def noise_pop():
        """Melee attack"""
        actions.mouse_click(1)

    def noise_cluck():
        """Block"""
        actions.key("c")

    def noise_hiss_start():
        """Dodge"""
        actions.key("space")

    def noise_shush_start():
        """Sprint"""
        actions.key("shift")

    def noise_hiss_stop():
        pass

    def noise_shush_stop():
        pass

    def foot_switch_top_down():
        actions.key("w:down")

    def foot_switch_top_up(held: bool):
        actions.key("w:up")

    def foot_switch_center_down():
        actions.key("s:down")

    def foot_switch_center_up(held: bool):
        actions.key("s:up")

    def foot_switch_left_down():
        actions.key("a:down")

    def foot_switch_left_up(held: bool):
        actions.key("a:up")

    def foot_switch_right_down():
        actions.key("d:down")

    def foot_switch_right_up(held: bool):
        actions.key("d:up")
