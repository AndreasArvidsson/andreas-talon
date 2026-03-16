from talon import Context, actions


# ---------- Non-sleep mode & tracker disabled ----------

ctx_eye_tracker = Context()
ctx_eye_tracker.matches = r"""
not mode: sleep
not tag: user.eye_tracker
and not tag: user.eye_tracker_frozen
"""


@ctx_eye_tracker.action_class("user")
class EyeTrackerOffActions:
    def foot_switch_right_down():
        actions.user.mouse_control_toggle(True)


# ---------- Non-sleep mode & tracker enabled/frozen ----------

ctx_eye_tracker_on = Context()
ctx_eye_tracker_on.matches = r"""
tag: user.eye_tracker
tag: user.eye_tracker_frozen
"""


@ctx_eye_tracker_on.action_class("user")
class EyeTrackerOnActions:
    def foot_switch_right_down():
        actions.user.mouse_freeze_toggle()

    @staticmethod
    def foot_switch_right_up(held: bool):
        if held:
            actions.user.mouse_freeze_toggle()


# ---------- Audio conferencing ----------

ctx_voip = Context()
ctx_voip.matches = r"""
mode: command
mode: dictation
mode: sleep
tag: user.voip
"""


@ctx_voip.action_class("user")
class VoipActions:
    def foot_switch_left_down():
        actions.user.mute_microphone()

    @staticmethod
    def foot_switch_left_up(held: bool):
        if held:
            actions.user.mute_microphone()
