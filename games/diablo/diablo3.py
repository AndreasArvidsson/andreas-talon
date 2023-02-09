from talon import Module, Context, actions

mod = Module()
ctx = Context()

mod.apps.diablo3 = """
os: windows
and app.exe: Diablo III64.exe
"""


ctx.matches = r"""
mode: user.game
app: diablo3
"""


@ctx.action_class("user")
class UserActions:
    def noise_pop():
        """Primary attack click"""
        actions.mouse_release(1)
        actions.mouse_click(0)

    def noise_cluck():
        """Secondary attack click"""
        actions.mouse_release(0)
        actions.mouse_click(1)

    def noise_hiss_start():
        """Primary attack hold"""
        actions.mouse_release(1)
        actions.mouse_drag(0)

    def noise_shush_start():
        """Secondary attack hold"""
        actions.mouse_release(0)
        actions.mouse_drag(1)

    # def noise_hiss_stop():
    #     actions.user.mouse_stop()

    # def noise_shush_stop():
    #     actions.user.mouse_stop()

    def foot_switch_top_down():
        """Start move"""
        actions.key("w:down")

    def foot_switch_top_up():
        """Stop move"""
        actions.key("w:up")

    def foot_switch_center_down():
        """Start stand still"""
        actions.key("shift:down")

    def foot_switch_center_up():
        """Stop stand still"""
        actions.key("shift:up")

    def foot_switch_left_down():
        """Toggle voice chat for game"""
        actions.user.game_toggle_mute()

    # def foot_switch_left_up():
    #     print("left up")

    # def foot_switch_right_down():
    #     print("right down")

    # def foot_switch_right_up():
    #     print("Right up")
