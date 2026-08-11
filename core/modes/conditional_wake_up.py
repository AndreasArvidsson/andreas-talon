from talon import Module, actions, cron

try:
    from talon import tracking_system
except Exception as e:
    print("Failed to import:", e)
    tracking_system = None


mod = Module()
gaze_detected: bool
event_triggered: bool


def on_gaze(e):
    global gaze_detected, event_triggered

    event_triggered = True

    if not e.gaze.zero():
        gaze_detected = True
        if tracking_system:
            tracking_system.unregister("gaze", on_gaze)


def evaluate_gaze_detection():
    if tracking_system:
        tracking_system.unregister("gaze", on_gaze)

    # Didn't get any gaze events from the eye tracker.
    # This can happen if the eye tracker is not working properly.
    if not event_triggered:
        return

    if not gaze_detected:
        print("No gaze detected, putting Talon to sleep")
        actions.user.talon_sleep()


@mod.action_class
class Actions:
    def eye_tracker_detect_gaze_or_sleep():
        """Put Talon to sleep if no gaze is detected, otherwise do nothing"""
        global gaze_detected, event_triggered

        if not tracking_system:
            return

        # No eye trackers are connected, do nothing
        if not tracking_system.trackers:
            return

        gaze_detected = False
        event_triggered = False

        tracking_system.register("gaze", on_gaze)

        cron.after("1s", evaluate_gaze_detection)
