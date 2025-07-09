# ----- Navigation -----
go <user.navigation_step>+:
    user.perform_navigation_steps(navigation_step_list)

page up:                    edit.page_up()
page down:                  edit.page_down()

go top:                     edit.file_start()
go bottom:                  edit.file_end()

head:                       edit.line_start()
tail:                       edit.line_end()
center:                     user.line_middle()

up:                         edit.up()
down:                       edit.down()
left:                       edit.left()
right:                      edit.right()

before:                     edit.word_left()
after:                      edit.word_right()

slap:                       edit.line_insert_down()
slapper:                    user.line_insert_down_twice()

indent:                     edit.indent_more()
dedent:                     edit.indent_less()

# ----- Selection -----
take all:                   edit.select_all()
take none:                  edit.select_none()

extend top:                 edit.extend_file_start()
extend bottom:              edit.extend_file_end()
extend head:                edit.extend_line_start()
extend tail:                edit.extend_line_end()

extend up:                  edit.extend_up()
extend down:                edit.extend_down()
extend left:                edit.extend_left()
extend right:               edit.extend_right()

extend before:              edit.extend_word_left()
extend after:               edit.extend_word_right()

# ----- Delete, undo, redo -----
undo:                       edit.undo()
redo:                       edit.redo()

deli:                       edit.delete_left()
drill:                      edit.delete_right()

remove:                     user.delete_word_left()
wipe:                       user.delete_word_right()

# ----- Cut, copy, paste -----
paste it:                   edit.paste()
paste special:              edit.paste_match_style()
paste insert:               user.insert_clipboard_with_keys()
paste as <user.formatters>: user.paste_clipboard_formatted(formatters)

# ----- Misc -----
drag up:                    edit.line_swap_up()
drag down:                  edit.line_swap_down()
disk:                       edit.save()

# ----- Text insertions -----
put to do:                  "TODO: "
put fix me:                 "FIXME: "
task:                       "- [ ] "
bullet:                     "* "
spam:                       ", "
stacker:                    ": "
period:                     ". "
dasher:                     " - "
arrow:                      user.insert_arrow()

# edit test insert:           user.edit_test_insert()
# edit test paste:            user.edit_test_paste()
# edit test paste text:       user.edit_test_paste_text()
# edit test paste performance:
#     user.edit_test_paste_text_performance()
