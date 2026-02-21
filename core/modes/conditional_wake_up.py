from talon import Module, cron, actions, tracking_system

mod = Module()

# True = gaze detected, False = no gaze detected, None = No gaze events
gaze_detected: bool | None


def on_gaze(e):
    global gaze_detected
    x, y = e.gaze

    if x or y:
        gaze_detected = True
        tracking_system.unregister("gaze", on_gaze)
    else:
        gaze_detected = False


def evaluate_gaze_detection():
    tracking_system.unregister("gaze", on_gaze)

    # Didn't get any gaze events from eye tracker.
    # This can happen if the eye tracker is not working properly.
    if gaze_detected is None:
        return

    if not gaze_detected:
        print("No gaze detected, putting Talon to sleep")
        actions.user.talon_sleep()


@mod.action_class
class Actions:
    def eye_tracker_detect_gaze_or_sleep():
        """Put Talon to sleep if no gaze is detected, otherwise do nothing"""
        global gaze_detected

        # No eye trackers are connected, do nothing
        if not tracking_system.trackers:
            return

        gaze_detected = None
        tracking_system.register("gaze", on_gaze)
        cron.after("1s", evaluate_gaze_detection)
