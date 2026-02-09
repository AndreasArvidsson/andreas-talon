from talon import Module, cron, actions, tracking_system

mod = Module()
gaze_detected = False


def on_gaze(e):
    global gaze_detected
    x, y = e.gaze

    if x or y:
        gaze_detected = True
        tracking_system.unregister("gaze", on_gaze)


def evaluate_gaze_status():
    tracking_system.unregister("gaze", on_gaze)

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

        gaze_detected = False
        tracking_system.register("gaze", on_gaze)
        cron.after("1s", evaluate_gaze_status)
