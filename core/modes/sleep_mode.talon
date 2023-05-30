mode: sleep
-

# settings():
#     speech.timeout = 0.1

parrot(cluck):
    user.debug("Talon wake parrot noise. Power: {power}")
    user.talon_wake()

# ^talon wake up$:
#     user.debug("Talon wake voice command")
#     user.talon_wake()

#this exists solely to prevent talon from waking up super easily in sleep mode at the moment with wav2letter
# <phrase>:                   skip()
