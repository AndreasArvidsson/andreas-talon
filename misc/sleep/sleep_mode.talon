mode: sleep
-

settings():
    speech.timeout = 0

^talon wake up$:
    user.debug("Talon wake voice command")
    user.talon_wake()

^talon status$:             user.talon_sleep_status()

#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
<phrase>:                   skip()
