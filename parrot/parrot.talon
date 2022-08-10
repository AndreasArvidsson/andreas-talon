mode: command
-

parrot(pop):
    print("pop")
    user.mouse_on_pop()
    # print(power)
    # print(ts)

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
