tag: user.file_manager
-
tag(): user.navigation
tag(): user.extensions

# ----- Navigation -----
go parent:                  user.file_manager_go_parent()
go home:                    user.file_manager_go_home()
go {user.path}:             user.file_manager_go(path)
go address:                 user.file_manager_focus_address()

open home:                  user.file_manager_open_home_new_tab()
open {user.path}:           user.file_manager_open_new_tab(path)

# ----- Create folders / files -----
file new:                   user.file_manager_new_file("")
folder new:                 user.file_manager_new_folder("")
file new <user.filename>$:  user.file_manager_new_file(filename)
folder new <user.filename>$: user.file_manager_new_folder(filename)

# ----- Miscellaneous -----
copy address:               user.file_manager_copy_address()
properties show:            user.file_manager_show_properties()
terminal here:              user.file_manager_terminal_here()
