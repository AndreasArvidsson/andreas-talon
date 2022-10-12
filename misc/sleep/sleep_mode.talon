mode: sleep
-

parrot(cluck):
    user.debug("Talon wake parrot noise. Power: {power}")
    # user.noise_throttle_pop(0.5) TODO
    user.talon_wake()

^talon wake up$:
    user.debug("Talon wake voice command")
    user.talon_wake()

^talon status$:             user.talon_sleep_status()

#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
<phrase>:                   skip()
