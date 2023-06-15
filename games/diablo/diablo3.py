from talon import Module, Context, actions

mod = Module()

mod.apps.diablo3 = """
os: windows
and app.exe: Diablo III64.exe
"""

mod.apps.diablo4 = """
os: windows
and app.exe: Diablo IV.exe
"""

ctx = Context()
ctx.matches = """
mode: user.game
app: diablo3
app: diablo4
"""

ctx_frozen_mouse = Context()
ctx_frozen_mouse.matches = """
mode: user.game
app: diablo3
app: diablo4
tag: user.eye_tracker_frozen
"""

# Release held mouse buttons for all key presses except these
dont_release = {"a", "b", "c", "d", "space"}


@ctx.action_class("main")
class MainActions:
    def key(key: str):
        """Diablo implementation of pressing a key"""
        if ":" not in key and key not in dont_release:
            actions.user.mouse_release_held_buttons()
        actions.next(key)


@ctx.action_class("user")
class UserActions:
    def noise_pop():
        """Primary attack hold"""
        mouse_click(0)
        actions.mouse_drag(0)

    def noise_cluck():
        """Secondary attack hold"""
        mouse_click(1)
        actions.mouse_drag(1)

    def noise_hiss_start():
        """Primary attack click"""
        mouse_click(0)

    def noise_shush_start():
        """Secondary attack click"""
        # mouse_click(1)
        actions.key("space")

    def noise_hiss_stop():
        pass

    def noise_shush_stop():
        pass

    def foot_switch_top_down():
        """Start move"""
        actions.user.mouse_release_held_buttons()
        actions.key("w:down")

    def foot_switch_top_up(held: bool):
        """Stop move"""
        actions.key("w:up")

    def foot_switch_center_down():
        """Start stand still"""
        actions.key("shift:down")

    def foot_switch_center_up(held: bool):
        """Stop stand still"""
        actions.key("shift:up")

    def foot_switch_left_down():
        """Toggle voice chat for game"""
        actions.user.game_toggle_mute()

    def foot_switch_left_up(held: bool):
        if held:
            actions.user.game_toggle_mute()

    def foot_switch_right_down():
        actions.user.mouse_freeze_toggle()

    def foot_switch_right_up(held: bool):
        actions.key("alt:up")
        if held:
            actions.user.mouse_freeze_toggle()


@ctx_frozen_mouse.action_class("user")
class FrozenMouseActions:
    def noise_pop():
        """Primary attack click"""
        mouse_click(0)

    def noise_cluck():
        """Secondary attack click"""
        mouse_click(1)

    def foot_switch_left_down():
        """Hold alt. Used for comparing rings"""
        actions.key("alt:down")

    def foot_switch_left_up(held: bool):
        actions.key("alt:up")


def mouse_click(button: int):
    # Can't hold two buttons at the same time
    actions.user.mouse_release_held_buttons()
    actions.mouse_click(button)
