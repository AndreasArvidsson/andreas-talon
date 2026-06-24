from talon import Module, speech_system, actions


mod = Module()


def on_pre_phrase(phrase):
    words = phrase.get("phrase")

    if not words:
        return

    gaze = actions.word.gaze(words[0])
    actions.tracking.control_always_on_toggle(False)
    speech_system.unregister("pre:phrase", on_pre_phrase)

    if not gaze:
        print("No gaze detected, putting Talon to sleep")
        actions.user.talon_sleep()


@mod.action_class
class Actions:
    def eye_tracker_detect_gaze_or_sleep():
        """Put Talon to sleep if no gaze is detected, otherwise do nothing"""

        # TODO: Figure out how to detect if no tracker is connected
        # # No eye trackers are connected, do nothing
        # if not tracking_system.trackers:
        #     return

        # actions.word.gaze requires always on
        actions.tracking.control_always_on_toggle(True)

        speech_system.register("pre:phrase", on_pre_phrase)
