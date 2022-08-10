mode: command
-

parrot(pop):
    print("pop")
    user.mouse_on_pop()

parrot(tsk):
    print("tsk")
    # user.mouse_click("control")

parrot(cluck):
    print("cluck")
    core.repeat_command(1)

parrot(shush):
    print("shush")
    user.mouse_scrolling("up")

parrot(hiss):
    print("hiss")
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
