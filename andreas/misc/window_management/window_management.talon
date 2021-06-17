^focus (help | show)$:                user.focus_toggle()
^focus {user.running_application}$:   user.focus_name(running_application)

^snap <user.window_snap_position>$:   user.snap_window(window_snap_position)
^snap next [screen]$:                 user.move_window_next_screen()
^snap last [screen]$:                 user.move_window_previous_screen()
^snap screen <number>:                user.move_window_to_screen(number)