not tag: user.gamepad_tester
-

gamepad(dpad_up):           print("dpad_up")
gamepad(dpad_down):         print("dpad_down")
gamepad(dpad_left):         print("dpad_left")
gamepad(dpad_right):        print("dpad_right")

gamepad(north):             print("north/Y")
gamepad(west):              print("west/X")
# gamepad(east):              print("east/B")
gamepad(east):              user.quick_pick_show()
gamepad(south):             print("south/A")

gamepad(select):            print("select/view")
gamepad(start):             print("start/menu")

gamepad(l1):                print("l1/Left bumper")
gamepad(r1):                print("r1/Right bumper")

# gamepad(l2:change):         print("l2/Left trigger {value}")
# gamepad(r2:change):         print("r2/Right trigger {value}")
gamepad(l2:change):         user.gamepad_scroll(0, value*-1)
gamepad(r2:change):         user.gamepad_scroll(0, value)

gamepad(l3):                print("l3/Left stick click")
gamepad(r3):                print("r3/Right stick click")

# gamepad(left_xy):           print("left_xy: {x}, {y}")
gamepad(left_xy):           user.gamepad_scroll(x, y*-1)
gamepad(right_xy):          print("right_xy: {x}, {y}")
# gamepad(right_x):           print("right_x: {value}")
# gamepad(right_y):           print("right_y: {value}")
