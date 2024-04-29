clippy:
    user.clippy_command_no_targets("showHide")

clippy {user.clippy_command_no_targets}:
    user.clippy_command_no_targets(clippy_command_no_targets)

clippy {user.clippy_command_with_targets} <user.clippy_targets>:
    user.clippy_command_with_targets(clippy_command_with_targets, clippy_targets)

clippy search <user.text>:
    user.clippy_search(text)

# paste <user.ordinals_small> [and <user.ordinals_small>]*:
#     user.clippy_paste(ordinals_small_list)

# clippy split <number_small> [and <number_small>]*:
#     user.clipboard_manager_split(number_small_list)
