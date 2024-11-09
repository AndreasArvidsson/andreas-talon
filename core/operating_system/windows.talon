os: windows
-
start menu:                 key(super)
context menu:               key(super-x)

scout app [<user.phrase>]$:
    key(super-s)
    insert("apps: {phrase or ''}")
pop app <user.phrase>$:
    key(super-s)
    insert("apps: {phrase}")
    key(enter)
