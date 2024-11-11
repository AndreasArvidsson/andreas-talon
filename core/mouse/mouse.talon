# Click
click {user.mouse_click}:   user.mouse_click(mouse_click)
drag:                       mouse_drag()
touch:                      user.mouse_click("left")
righter:                    user.mouse_click("right")
midd:                       user.mouse_click("middle")
con:                        user.mouse_click("control")

# Scroll
climb:                      user.mouse_scroll_up_continuous()
drop:                       user.mouse_scroll_down_continuous()
climb <number_small>:       user.mouse_scroll_up(number_small)
drop <number_small>:        user.mouse_scroll_down(number_small)
mouse gaze:                 user.mouse_gaze_scroll()

# Eye tracking
track on:                   user.mouse_control_toggle(true)
track off:                  user.mouse_control_toggle(false)
tracking:                   user.mouse_control_toggle()
track gaze:                 tracking.control_gaze_toggle(true)
track head:                 tracking.control_gaze_toggle(false)
track debug:                tracking.control_debug_toggle()
track calibrate:            tracking.calibrate()

# Cursor
cursor center:              user.mouse_move_center_window()
cursor print:               print("{mouse_x()}, {mouse_y()}")
cursor copy:                clip.set_text("{mouse_x()}, {mouse_y()}")
# ^cursor show$:              user.mouse_show_cursor()
# ^cursor hide$:              user.mouse_hide_cursor()
