clippy:
    user.clippy_command_no_targets("toggleShowHide")

clippy search <user.prose>:
    user.clippy_search(prose)

clippy {user.clippy_command_no_targets}:
    user.clippy_command_no_targets(clippy_command_no_targets)

clippy {user.clippy_command_with_targets} <user.clippy_targets>:
    user.clippy_command_with_targets(clippy_command_with_targets, clippy_targets)

clippy rename <user.clippy_targets>:
    user.clippy_rename(clippy_targets)

clippy rename <user.clippy_targets> as <user.prose>:
    user.clippy_rename(clippy_targets, prose)

clippy get <user.clippy_targets>:
    user.clippy_get(clippy_targets)

[clippy] paste <user.ordinals_small> [and <user.ordinals_small>]*:
    user.clippy_paste_indices(ordinals_small_list)
