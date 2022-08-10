from talon import cron, Module, ctrl
from typing import Callable
import numpy as np


class PowerMomentum:
    job = None
    cb: Callable[[float], None]
    momentum_increasing = True
    momentum: float = 0.1
    starting_ts: float = 0
    power_scaling = 2.0

    def __init__(self):
        self.job = None
        self.cb = lambda momentum: print(f"{momentum:.1f}")

    def set_callback(self, cb: Callable):
        """Set the callback that will be triggered with each momentum update"""
        self.cb = cb

    def start(self, ts):
        """Start building momentum"""
        self.starting_ts = ts
        cron.cancel(self.job)
        self.momentum_increasing = True
        self.momentum = max(0.1, self.momentum)
        self.job = cron.interval("16ms", self.momentum_job)

    def mark_decay(self):
        """Mark the momentum as no longer increasing"""
        self.starting_ts = 0
        self.momentum_increasing = False

    def stop(self):
        """Stop all momentum immediately"""
        self.momentum = 0
        self.momentum_increasing = False
        cron.cancel(self.job)
        self.cb(self.momentum)

    def add_momentum(self, ts: float, power: float):
        """Increase the momentum based on the duration of the sound and the power"""
        duration_ms = (ts - self.starting_ts) * 1000

        # For short duration sounds, make the power count more towards the momentum value
        if duration_ms / 130 < 1:
            self.momentum += power * self.power_scaling / 2

        # For any duration longer than 130 milliseconds, increase the momentum more and more over time
        else:
            self.momentum += (power * self.power_scaling / 5) * np.sqrt(
                [duration_ms / 100]
            )[0]

    def momentum_job(self):
        self.momentum = self.momentum * 0.9765
        if (
            self.momentum_increasing == False
            and self.momentum < 0.5
            or self.momentum == 0.0
        ):
            self.momentum = 0
            cron.cancel(self.job)
        self.cb(self.momentum)


power_momentum = PowerMomentum()

float_scrolling_allowed = True
# Scrolling code
scroll_tick_index = 0
scroll_tick_thresholds = [
    1,
    0.99,
    0.96,
    0.93,
    0.90,
    0.85,
    0.80,
    0.75,
    0.70,
    0.60,
    0.45,
    0.33,
    0.0,
]
previous_scroll = 0


def scroll_momentum(momentum: float):
    global scroll_tick_index, previous_scroll
    scroll = momentum / 20
    if not float_scrolling_allowed and scroll > previous_scroll:
        for index, value in enumerate(scroll_tick_thresholds):
            if value < scroll:
                scroll_tick_index = index
                break
    previous_scroll = scroll

    if scroll < 1 and not float_scrolling_allowed:
        scroll = 1 if scroll < scroll_tick_thresholds[scroll_tick_index] else 0
        if scroll == 1:
            scroll_tick_index = min(
                len(scroll_tick_thresholds) - 1, scroll_tick_index + 1
            )
    return scroll


def scroll_up(momentum: float):
    scroll = scroll_momentum(momentum)
    ctrl.mouse_scroll(-int(scroll), by_lines=False)


def scroll_down(momentum: float):
    scroll = scroll_momentum(momentum)
    ctrl.mouse_scroll(int(scroll), by_lines=False)


mod = Module()


@mod.action_class
class Actions:
    def power_momentum_start(ts: float, power_scaling: float):
        """Start building momentum with the scaling factor"""
        global power_momentum
        power_momentum.power_scaling = power_scaling
        power_momentum.start(ts)

    def power_momentum_stop():
        """Instantaniously stop the momentum"""
        global power_momentum
        power_momentum.stop()

    def power_momentum_add(ts: float, power: float):
        """Increase the momentum by adding time and power"""
        global power_momentum
        power_momentum.add_momentum(ts, power)

    def power_momentum_decaying():
        """Mark the momentum as in a decaying state"""
        global power_momentum
        power_momentum.mark_decay()

    def power_momentum_scroll_down():
        """Set the power momentum callback to a scrolling down function"""
        global power_momentum
        power_momentum.set_callback(scroll_down)

    def power_momentum_scroll_up():
        """Set the power momentum callback to a scrolling up function"""
        global power_momentum
        power_momentum.set_callback(scroll_up)
