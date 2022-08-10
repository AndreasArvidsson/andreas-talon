mode: command
-

parrot(pop):                user.mouse_on_pop()
# parrot(tsk):                user.mouse_click("control")

parrot(cluck):              core.repeat_command(1)

parrot(shush):              user.mouse_scrolling("up")
parrot(hiss):               user.mouse_scrolling("down")

parrot(shush:stop):         user.mouse_stop()
parrot(hiss:stop):          user.mouse_stop()
