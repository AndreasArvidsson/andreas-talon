mode: sleep
-

settings():
    speech.timeout = 0

^talon wake$:   user.talon_wake()

#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
<phrase>:       skip()