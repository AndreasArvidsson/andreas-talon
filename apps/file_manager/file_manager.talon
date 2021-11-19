tag: user.file_manager
-

# ----- Navigation -----
go back:                   user.go_back()
go forward:                user.go_forward()
go up:                     user.file_manager_go_parent()
go address:                user.file_manager_focus_address()
go {user.path}:            user.file_manager_open_directory(path)
copy address:              user.file_manager_copy_address()

# ----- Create folders / files -----
file new:                  user.file_manager_new_file("")
folder new:                user.file_manager_new_folder("")
file new <user.text>$:     user.file_manager_new_file(text)
folder new <user.text>$:   user.file_manager_new_folder(text)

# ----- Miscellaneous -----
properties show:           user.file_manager_show_properties()
terminal here:             user.file_manager_terminal_here()