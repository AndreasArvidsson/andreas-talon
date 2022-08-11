mode: command
-

parrot(pop):
    user.debug("pop")
    user.mouse_on_pop()

# parrot(tsk):
    # user.debug("tsk")
    # user.mouse_click("control")

parrot(cluck):
    user.debug("cluck")
    core.repeat_command(1)

parrot(shush):
    user.debug("shush")
    user.mouse_scrolling("up")

parrot(hiss):
    user.debug("hiss")
    user.mouse_scrolling("down")

parrot(shush:stop):         user.mouse_stop()
parrot(hiss:stop):          user.mouse_stop()


# parrot(hiss):
#     user.power_momentum_scroll_down()
#     user.power_momentum_start(ts, 5.0)
# parrot(hiss:repeat):
#     user.power_momentum_add(ts, power)
# parrot(hiss:stop):
#     user.power_momentum_decaying()
#     # user.power_momentum_stop()
