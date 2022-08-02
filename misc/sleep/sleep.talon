mode: command
mode: dictation
language: en_US
language: sv_SE
-
settings():
    user.sleep_word = "drowse"

drowse [<phrase>]$:         user.talon_sleep()
^talon sleep$:              user.talon_sleep()
^talon status$:             user.talon_sleep_status()
