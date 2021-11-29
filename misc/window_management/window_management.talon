focus {user.running_application}:
    user.focus_name(running_application)

(focus {user.running_application} <phrase>)+$:
    user.focus_names(running_application_list, phrase_list)

window new:                         app.window_open()
window close:                       app.window_close()
window last:                        app.window_previous()
window next:                        app.window_next()
window back:                        key("alt-tab")

snap <user.window_snap_position>:   user.snap_window(window_snap_position)
snap next [screen]:                 user.move_window_next_screen()
snap last [screen]:                 user.move_window_previous_screen()
snap screen <number_small>:         user.move_window_to_screen(number_small)

move center:                        user.move_window_to_screen_center()
move {user.resize_side} {user.resize_direction} [{user.resize_size}]:
    user.resize_window(resize_side, resize_direction, resize_size or "medium")

screen numbers:                     user.screens_show_numbering()