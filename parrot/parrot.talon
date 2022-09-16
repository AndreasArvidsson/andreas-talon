not mode: sleep
-

# parrot(pop):
#     user.debug("pop {power}")
#     user.noise_pop()

parrot(cluck):
    user.debug("cluck {power}")
    user.noise_cluck()
    user.noise_throttle_pop(0.2)

parrot(shush):              user.noise_debounce("shush", 1)
parrot(shush:stop):         user.noise_debounce("shush", 0)

parrot(hiss):               user.noise_debounce("hiss", 1)
parrot(hiss:stop):          user.noise_debounce("hiss", 0)
