^focus (help | show)$:                user.focus_toggle()
^focus {user.running_application}$:   user.focus_name(running_application)

window new:                           app.window_open()
window close:                         app.window_close()
window (previous | prev):             app.window_previous()
window next:                          app.window_next()
window last:                          key("alt-tab")

^snap <user.window_snap_position>$:   user.snap_window(window_snap_position)
^snap next [screen]$:                 user.move_window_next_screen()
^snap last [screen]$:                 user.move_window_previous_screen()
^snap screen <number>:                user.move_window_to_screen(number)