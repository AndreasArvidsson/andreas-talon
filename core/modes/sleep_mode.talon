mode: sleep
-

# settings():
#     speech.timeout = 0.1

parrot(cluck):
    user.debug("Talon wake parrot noise. Power: {power}")
    user.talon_wake()
    user.eye_tracker_detect_gaze_or_sleep()

# ^talon wake up$:
#     user.debug("Talon wake voice command")
#     user.talon_wake()

#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
# <phrase>:                   skip()
