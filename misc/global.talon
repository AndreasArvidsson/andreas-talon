then:                       skip()
stop:                       user.stop_app()

pick <number_small>:        user.pick_item(number_small)
pick to:                    user.pick_item(2)
pick <user.word>:
    "{word}"
    key(enter)
pick <user.letters>:
    "{letters}"
    key(enter)

start recording:
    user.command_history_clear()
    user.talon_sleep_no_notification()
    user.recording_start()

stop recording:
    user.recording_stop()
