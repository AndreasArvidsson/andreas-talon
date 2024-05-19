clippy:
    user.clippy_command_no_targets("showHide")

clippy search <user.text>:
    user.clippy_search(text)

clippy {user.clippy_command_no_targets}:
    user.clippy_command_no_targets(clippy_command_no_targets)

clippy {user.clippy_command_with_targets} <user.clippy_targets>:
    user.clippy_command_with_targets(clippy_command_with_targets, clippy_targets)

clippy rename <user.clippy_targets>:
    user.clippy_rename(clippy_targets)

clippy rename <user.clippy_targets> as <user.text>:
    user.clippy_rename(clippy_targets, text)

[clippy] paste <user.clippy_targets>:
    user.clippy_command_with_targets("pasteItems", clippy_targets)

[clippy] paste <user.ordinals_small> [and <user.ordinals_small>]*:
    user.clippy_paste_indices(ordinals_small_list)

clippy get <user.clippy_targets>:
    user.clippy_get(clippy_targets)

# clippy split <number_small> [and <number_small>]*:
#     user.clipboard_manager_split(number_small_list)
