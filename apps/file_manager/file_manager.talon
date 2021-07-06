tag: user.file_manager
-

# ----- Navigation -----
go back:                    user.file_manager_go_back()
go forward:                 user.file_manager_go_forward()
go up:                      user.file_manager_go_parent()
go address:                 user.file_manager_focus_address()
go {user.path}:             user.file_manager_open_directory(path)
copy address:               user.file_manager_copy_address()

# ----- Create folders / files -----
file new [<user.text>]:     user.file_manager_new_file(text or '')
folder new [<user.text>]:   user.file_manager_new_folder(text or '')

# ----- Miscellaneous -----
properties show:            user.file_manager_show_properties()
terminal here:              user.file_manager_terminal_here()