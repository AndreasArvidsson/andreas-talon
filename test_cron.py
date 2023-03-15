from talon import cron, speech_system
import time

t1 = 0


def on_interval():
    global t1
    t2 = time.perf_counter()
    print(f"{(t2-t1)*1000}ms")
    t1 = t2


# cron.interval("16ms", on_interval)
# speech_system.register("pre:phrase", lambda _: print("########## phrase ##########"))
