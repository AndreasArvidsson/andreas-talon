os: windows
-
start menu:                 key(super)
context menu:               key(super-x)

scout app [<user.prose>]$:
    key(super-s)
    insert("apps: {prose or ''}")
pop app <user.prose>$:
    key(super-s)
    insert("apps: {prose}")
    key(enter)
