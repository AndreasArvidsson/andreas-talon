tag: user.tabs
-

tab prev:                 app.tab_previous()
tab prev <number_small>:
	app.tab_previous()
	repeat(number_small - 1)
tab next:                 app.tab_next()
tab next <number_small>:
	app.tab_next()
	repeat(number_small - 1)
tab <user.digit>:         user.tab_jump(digit)
tab final:                user.tab_final()

tab left:                 user.tab_move_left()
tab right:                user.tab_move_right()

tab (new | open):         app.tab_open()
tab duplicate:            user.tab_duplicate()
tab close:                app.tab_close()
tab (reopen | restore):   app.tab_reopen()

tab mute:                 user.tab_mute()