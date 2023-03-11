os: windows
-

show desktop:               key(super-d)
switcher:                   key(ctrl-alt-tab)
task view:                  key(super-tab)
start menu:                 key(super)
context menu:               key(super-x)

scout app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
pop app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
    key(enter)
