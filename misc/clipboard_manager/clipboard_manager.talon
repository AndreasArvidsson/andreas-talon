mode: user.clipboard_manager
-

clip hide:     user.clipboard_manager_toggle()

clip update:   user.clipboard_manager_update()

clip clear:    user.clipboard_manager_remove()

clip chuck <number_small> [and <number_small>]*:
    user.clipboard_manager_remove(number_small_list)

clip split <number_small> [and <number_small>]*:
    user.clipboard_manager_split(number_small_list)

paste <number_small> [and <number_small>]*:
    user.clipboard_manager_paste(number_small_list)
paste special <number_small> [and <number_small>]*:
    user.clipboard_manager_paste(number_small_list, 1)