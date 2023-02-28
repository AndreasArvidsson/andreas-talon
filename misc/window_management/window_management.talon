window new:                 app.window_open()
window close:               app.window_close()
window hide:                app.window_hide()
window last:                app.window_previous()
window next:                app.window_next()
window back:                user.window_focus_last()

focus {user.running_application}:
    user.window_focus_name(running_application)

snap <user.screen>:
    user.window_snap_to_screen(screen)

snap {user.window_snap_position}:
    user.window_snap_to_position(window_snap_position)

snap <user.screen> {user.window_snap_position}:
    user.window_snap_to_screen_and_position(screen, window_snap_position)

snap {user.running_application}:
    user.window_swap_positions_with_app(running_application)

move center:                user.window_move_to_screen_center()
move side:                  user.window_resize_at_cursor_position()
move here:                  user.window_move_at_cursor_position()

move {user.resize_side} {user.resize_direction} [{user.resize_size}]:
    user.window_resize(resize_side, resize_direction, resize_size or "medium")

(snap | move) back:         user.window_revert_rect()

screen numbers:             user.screens_show_numbering()
