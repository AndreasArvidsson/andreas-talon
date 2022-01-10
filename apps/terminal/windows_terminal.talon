app: windows_terminal
-
tag(): user.tabs
tag(): user.bash

split auto:     key(ctrl-alt-d)
split right:    key(ctrl-alt-right)
split down:     key(ctrl-alt-down)

focus up:       key(alt-up)
focus down:     key(alt-down)
focus left:     key(alt-left)
focus right:    key(alt-right)

resize up:      key(alt-shift-up)
resize down:    key(alt-shift-down)
resize left:    key(alt-shift-left)
resize right:   key(alt-shift-right)

please:         key(ctrl-shift-p)
please <user.text>$:
    key(ctrl-shift-p)
    "{text}"