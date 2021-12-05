mode: user.help_commands
-

help hide:             user.help_hide()
help <number_small>:   user.help_select_index(number_small - 1)
help last:             user.help_previous()
help next:             user.help_next()
help return:           user.help_return()