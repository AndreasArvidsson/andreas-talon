not app: vscode
-

take line:               edit.select_line()
chuck line:              edit.delete_line()
clear line:              user.clear_line()
copy line:               user.copy_line()
cut line:                user.cut_line()
clone line:              edit.line_clone()

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