from talon import Module
import time

mod = Module()

hold_timeout = 0.2

t1 = 0
count = 0
last = ""


@mod.action_class
class Actions:
    def parrot_test(name: str):
        """"""
        global t1, count, last
        if last != name:
            count = 1
            last = name

        delta = round((time.monotonic() - t1) * 1000)
        print(f"{count} {name} {delta}")
        count += 1
        t1 = time.monotonic()
