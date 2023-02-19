mode: command
mode: dictation
language: en
language: sv
-

{user.sleep_phrase} [<phrase>]$:
    user.talon_sleep_command()

^talon status$:             user.talon_sleep_status()
