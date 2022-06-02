clippy:   user.clipboard_manager_toggle()

paste <number_small> [and <number_small>]*:
    user.clipboard_manager_paste(number_small_list)

paste special <number_small> [and <number_small>]*:
    user.clipboard_manager_paste(number_small_list, 1)
