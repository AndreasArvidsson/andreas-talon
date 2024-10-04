app: windows_explorer
app: windows_file_browser
-
tag(): user.file_manager
tag(): user.tabs

go up:                      user.select_up()
go down:                    user.select_down()
select:                     user.select_toggle()
file rename:                key(f2)
file remove:                key(delete)

open home:
    app.tab_open()
    user.file_manager_go_home()
open {user.path}:
    app.tab_open()
    user.file_manager_go(path)

file copy name:
    key(f2)
    edit.copy()
    key(enter)

scout [<user.text>]$:
    edit.find(text or "")
pop <user.text>$:
    edit.find(text)
    sleep(100ms)
    key(enter)
