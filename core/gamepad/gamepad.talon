not tag: user.gamepad_tester
-

gamepad(dpad_up):           edit.up()
gamepad(dpad_down):         edit.down()
gamepad(dpad_left):         edit.left()
gamepad(dpad_right):        edit.right()

gamepad(north):             user.mouse_click("control")
gamepad(west):              user.mouse_drag()
gamepad(east):              user.mouse_click("right")
gamepad(south):             user.mouse_freeze_toggle()

gamepad(select):            user.quick_pick_show()
gamepad(start):             user.command_dictation_mode_toggle()

gamepad(l1):                user.go_back()
gamepad(r1):                user.go_forward()

gamepad(l2:change):         user.gamepad_scroll(0, value*-1)
gamepad(r2:change):         user.gamepad_scroll(0, value)

gamepad(left_xy):           user.gamepad_scroll(x, y*-1)
gamepad(l3):                user.gamepad_scroll_slow_toggle()

gamepad(right_xy):          print("right_xy: {x}, {y}")
gamepad(r3):                print("r3/Right stick click")
