app: windows_explorer
app: windows_file_browser
-
tag(): user.file_manager

compress archive:       key(menu a)
scout [<user.text>]$:   edit.find(text or "")
pop <user.text>$:
    edit.find(text)
    sleep("100ms")
    key(enter)
