mode: command
mode: dictation
language: en
language: sv
-

{user.sleep_phrase} [<phrase>]$:
    user.debug("Talon sleep voice command")
    user.talon_sleep()

^talon status$:             user.talon_sleep_status()
