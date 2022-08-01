# Click
click {user.mouse_click}:   user.mouse_click(mouse_click)
mouse drag:                 user.mouse_drag()
click center:
    user.mouse_center_window()
    mouse_click(0)

# Scroll
climb:                      user.mouse_scrolling("up")
drop:                       user.mouse_scrolling("down")
climb <number_small>:       user.mouse_scroll("up", number_small)
drop <number_small>:        user.mouse_scroll("down", number_small)
mouse gaze:                 user.mouse_gaze_scroll()

mouse speed show:           user.mouse_scroll_speed_notify()
mouse speed <number_small>: user.mouse_scroll_speed_set(number_small)
mouse speed up:             user.mouse_scroll_speed_increase()
mouse speed down:           user.mouse_scroll_speed_decrease()

# Eye tracking
track control:              user.mouse_toggle_control_mouse()
track zoom:                 user.mouse_toggle_zoom_mouse()
track off:                  user.mouse_turn_off()
^track calibrate$:          tracking.calibrate()
^track debug$:              tracking.control_debug_toggle()

# Cursor
cursor center:              user.mouse_center_window()
cursor print:               print("{mouse_x()}, {mouse_y()}")
cursor copy:                clip.set_text("{mouse_x()}, {mouse_y()}")
^cursor show$:              user.mouse_show_cursor()
^cursor hide$:              user.mouse_hide_cursor()
