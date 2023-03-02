window new:                 app.window_open()
window close:               app.window_close()
window hide:                app.window_hide()
window last:                app.window_previous()
window next:                app.window_next()
window back:                user.window_focus_last()

focus {user.running_application}:
    user.window_focus_name(running_application)

snap <user.screen>:
    user.snap_active_window_to_screen(screen)
snap {user.snap_position}:
    user.snap_active_window_to_position(snap_position)
snap <user.screen> {user.snap_position}:
    user.snap_active_window_to_screen_and_position(screen, snap_position)

snap this <user.screen>:
    user.snap_window_under_cursor_to_screen(screen)
snap this {user.snap_position}:
    user.snap_window_under_cursor_to_position(snap_position)
snap this <user.screen> {user.snap_position}:
    user.snap_window_under_cursor_to_screen_and_position(screen, snap_position)

snap {user.running_application} <user.screen>:
    user.snap_application_to_screen(running_application, screen)
snap {user.running_application} {user.snap_position}:
    user.snap_application_to_position(running_application, snap_position)
snap {user.running_application} <user.screen> {user.snap_position}:
    user.snap_application_to_screen_and_position(running_application, screen, snap_position)

(snap | move) back:
    user.window_revert_active()
(snap | move) this back:
    user.window_revert_under_cursor()
(snap | move) {user.running_application} back:
    user.window_revert_application(running_application)

snap {user.running_application}:
    user.window_swap_positions_with_app(running_application)

move center:                user.window_move_to_screen_center()
side here:                  user.window_resize_at_cursor_position()
move here:                  user.window_move_at_cursor_position()

move {user.resize_side} {user.resize_direction} [{user.resize_size}]:
    user.window_resize(resize_side, resize_direction, resize_size or "medium")

screen numbers:             user.screens_show_numbering()
