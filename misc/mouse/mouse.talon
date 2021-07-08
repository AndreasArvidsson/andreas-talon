# Buttons
mouse {user.mouse_click}:   user.mouse_click(mouse_click)
mouse drag:                 user.mouse_drag()

# Scroll
scroll up [<number>]:       user.mouse_scroll("up", number or 1)
scroll down [<number>]:     user.mouse_scroll("down", number or 1)
# TODO
# mouse up:                   user.mouse_scrolling("up")
# (mouse down | mouston):     user.mouse_scrolling("down")
climb:                      user.mouse_scrolling("up")
fall:                       user.mouse_scrolling("down")

mouse speed show:           user.mouse_print_scroll_speed()
mouse speed <number>:       user.mouse_scroll_speed(number)
mouse speed inc:            user.mouse_scroll_increase()
mouse speed desc:           user.mouse_scroll_decrease()

mouse gaze:                 user.mouse_gaze_scroll()

# Misc
^mouse calibrate$:          user.mouse_calibrate()
^mouse control mode$:       user.mouse_toggle_control_mouse()
^mouse zoom$:               user.mouse_toggle_zoom_mouse()

# Say esc to cancel zoom or scroll