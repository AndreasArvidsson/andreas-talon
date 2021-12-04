not app: vscode
-

take line:               edit.select_line()
pre line:                edit.line_start()
post line:               edit.line_end()
chuck line:              edit.delete_line()
clear line:              user.clear_line()
copy line:               user.copy_line()
cut line:                user.cut_line()

clone line:              edit.line_clone()
drink (line | this):     edit.line_insert_up()
pour (line | this):      edit.line_insert_down()

take head:               user.select_line_start()
take tail:               user.select_line_end()
(chuck | clear) head:    user.delete_line_start()
(chuck | clear) tail:    user.delete_line_end()
copy head:               user.copy_line_start()
copy tail:               user.copy_line_end()
cut head:                user.cut_line_start()
cut tail:                user.cut_line_end()

take block:              edit.select_paragraph()
pre block:               edit.paragraph_start()
post block:              edit.paragraph_end()
(chuck | clear) block:   edit.delete_paragraph()
copy block:              user.copy_paragraph()
cut block:               user.cut_paragraph()

take file:               edit.select_all()
pre file:                edit.file_start()
post file:               edit.file_end()
(chuck | clear) file:    user.delete_all()
copy file:               user.copy_all()
cut file:                user.cut_all()


# ----- Navigate to specified text/symbol: go right paren
{user.navigation_action} {user.navigation_direction} to <user.any_alphanumeric_key>:
    user.navigation(navigation_action, navigation_direction, any_alphanumeric_key)