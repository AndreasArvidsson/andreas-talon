app: clippy
-

dev tools:
    user.clippy_command_no_targets("toggleDevTools")

{user.clippy_command_with_targets} <user.clippy_targets>:
    user.clippy_command_with_targets(clippy_command_with_targets, clippy_targets)
