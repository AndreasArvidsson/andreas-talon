mode: command
mode: dictation
mode: user.game
-

parrot(pop):
    # user.debug("pop {power}")
    user.noise_pop()

parrot(cluck):
    # user.debug("cluck {power}")
    user.noise_cluck()

parrot(shush):
    # user.debug("shush {power}")
    user.noise_debounce("shush", true)
parrot(shush:stop):         user.noise_debounce("shush", false)

parrot(hiss):
    # user.debug("hiss {power}")
    user.noise_debounce("hiss", true)
parrot(hiss:stop):          user.noise_debounce("hiss", false)
