# Click
click {user.mouse_click}:   user.mouse_click(mouse_click)
drag:                       user.mouse_drag()
con:                        user.mouse_click("control")
righter:                    user.mouse_click("right")

# Scroll
climb:                      user.mouse_scrolling("up")
drop:                       user.mouse_scrolling("down")
climb <number_small>:       user.mouse_scroll("up", number_small)
drop <number_small>:        user.mouse_scroll("down", number_small)
mouse gaze:                 user.mouse_gaze_scroll()

scroll speed show:          user.mouse_scroll_speed_notify()
scroll speed <number_small>: user.mouse_scroll_speed_set(number_small)
scroll speed up:            user.mouse_scroll_speed_increase()
scroll speed down:          user.mouse_scroll_speed_decrease()

# Eye tracking
track on:                   user.mouse_control_toggle(true)
track off:                  user.mouse_control_toggle(false)
tracking:                   user.mouse_control_toggle()
^track calibrate$:          tracking.calibrate()
^track debug$:              tracking.control_debug_toggle()

# Cursor
cursor center:              user.mouse_center_window()
cursor print:               print("{mouse_x()}, {mouse_y()}")
cursor copy:                clip.set_text("{mouse_x()}, {mouse_y()}")
# ^cursor show$:              user.mouse_show_cursor()
# ^cursor hide$:              user.mouse_hide_cursor()
