not tag: user.gamepad_tester
-

gamepad(dpad_up):           edit.up()
gamepad(dpad_down):         edit.down()
gamepad(dpad_left):         edit.left()
gamepad(dpad_right):        edit.right()

gamepad(west:down):         mouse_drag()
gamepad(west:up):           mouse_release()
gamepad(north:down):        mouse_drag(1)
gamepad(north:up):          mouse_release(1)
gamepad(east):              user.mouse_click("control")
gamepad(south:down):        user.gamepad_mouse_freeze(true)
gamepad(south:up):          user.gamepad_mouse_freeze(false)

gamepad(select):            user.quick_pick_show()
gamepad(start):             user.command_dictation_mode_toggle()

gamepad(l1):                user.go_back()
gamepad(r1):                user.go_forward()

gamepad(l2:change):         user.gamepad_scroll(0, value*-1)
gamepad(r2:change):         user.gamepad_scroll(0, value)

gamepad(left_xy):           user.gamepad_scroll(x, y*-1)
gamepad(l3):                user.gamepad_scroll_slow_toggle()

gamepad(right_xy:repeat):   user.gamepad_mouse_move(x, y*-1)
gamepad(r3):                user.gamepad_mouse_move_slow_toggle()
