from talon import Module, actions, cron


REPEAT_DELAY = "250ms"
REPEAT_RATE = "32ms"

mod = Module()
repeated_key_jobs = {}


@mod.action_class
class Actions:
    def key_hold(key: str):
        """Simulate holding a key with repeated key presses"""
        actions.key(key)

        def add_interval():
            repeated_key_jobs[key] = cron.interval(
                REPEAT_RATE,
                lambda: actions.key(key),
            )

        repeated_key_jobs[key] = cron.after(REPEAT_DELAY, add_interval)

    def key_release(key: str):
        """Stop repeating key"""
        job = repeated_key_jobs.get(key)

        if job is not None:
            cron.cancel(job)
            repeated_key_jobs[key] = None
