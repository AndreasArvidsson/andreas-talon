tag: user.tabs
-

tab last:                 app.tab_previous()
tab last <number_small>:
    app.tab_previous()
    repeat(number_small - 1)
tab next:                 app.tab_next()
tab next <number_small>:
    app.tab_next()
    repeat(number_small - 1)
tab <user.digit>:         user.tab_jump(digit)
tab final:                user.tab_final()
tab back:                 user.tab_back()
tab left:                 user.tab_move_left()
tab right:                user.tab_move_right()
tab new:                  app.tab_open()
tab duplicate:            user.tab_duplicate()
tab (reopen | restore):   app.tab_reopen()

tab close:                app.tab_close()
tab <user.digit> close:
    user.tab_jump(digit)
    app.tab_close()