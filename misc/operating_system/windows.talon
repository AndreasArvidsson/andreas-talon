os: windows
-

task view:                    key(super-tab)
task manager:                 key(ctrl-shift-escape)
switcher:                     key(ctrl-alt-tab)
show desktop:                 key(super-d)

start menu:                   key(super)
context menu:                 key(super-x)

open {user.launch_command}:   user.exec(launch_command)

(start | stop) recording:     key(alt-f9)

scout app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
pop app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
    key(enter)