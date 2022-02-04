mode: command
mode: dictation
-
settings():
    user.sleep_word = "drowse"

drowse [<phrase>]$:   user.talon_sleep()
^talon sleep$:        user.talon_sleep()
^talon status$:       user.talon_sleep_status()