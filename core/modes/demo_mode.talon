mode: user.demo
-

settings():
    user.subtitles_show = false

parrot(pop):
    user.mouse_on_pop()

command mode$:
    user.command_mode()

start recording:
    user.clear_subtitles()
    user.recording_start()

stop recording:
    user.recording_stop()

<phrase>:                   skip()
