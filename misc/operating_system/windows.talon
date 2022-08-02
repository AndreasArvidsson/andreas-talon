os: windows
-

show desktop:               key(super-d)
switcher:                   key(ctrl-alt-tab)

open task manager:          key(ctrl-shift-escape)

task view:                  key(super-tab)
start menu:                 key(super)
context menu:               key(super-x)

(start | stop) recording:   key(alt-f9)

scout app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
pop app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
    key(enter)
