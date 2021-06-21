mode: command
mode: dictation
-

# ----- Navigation -----
page up:                           edit.page_up()
page down:                         edit.page_down()

peak:                              edit.file_start()
bottom:                            edit.file_end()

head:                              edit.line_start()
tail:                              edit.line_end()
middle:                            user.line_middle()

up [<number_small>]:               user.up(number_small or 1)
down [<number_small>]:             user.down(number_small or 1)
left [<number_small>]:             user.left(number_small or 1)
right [<number_small>]:            user.right(number_small or 1)

lefter [<number_small>]:           user.word_left(number_small or 1)
righter [<number_small>]:          user.word_right(number_small or 1)

slap:                              edit.line_insert_down()
slapper:                           user.line_insert_down(2)

indent:                            edit.indent_more()
dedent:                            edit.indent_less()

# ----- Navigate to specified text/symbol: go right paren
{user.navigation_action} {user.navigation_direction} to <user.text_symbol>:
	user.navigation(navigation_action, navigation_direction or "right", text_symbol)

# ----- Selection -----
select all:                        edit.select_all()
select none:                       edit.select_none()
select line:                       edit.select_line()
select word:                       edit.select_word()

select peak:                       edit.extend_file_start()
select bottom:                     edit.extend_file_end()
select head:                       edit.extend_line_start()
select tail:                       edit.extend_line_end()

select up [<number_small>]:        user.extend_up(number_small or 1)
select down [<number_small>]:      user.extend_down(number_small or 1)
select left [<number_small>]:      user.extend_left(number_small or 1)
select right [<number_small>]:     user.extend_right(number_small or 1)

select lefter [<number_small>]:    user.extend_word_left(number_small or 1)
select righter [<number_small>]:   user.extend_word_right(number_small or 1)

# ----- Delete, undo, redo -----
(undo it | nope):                  edit.undo()
redo it:                           edit.redo()

(del | delete):                    edit.delete()
delfor:                            user.delete_right()

remove:                            edit.delete_word()
remfor:                            user.delete_word_right()

scratch line:                      edit.delete_line()
scratch head:                      user.delete_line_start()
scratch tail:                      user.delete_line_end()
clear line:                        user.clear_line()

# ----- Cut, copy, paste -----
cut it:                            edit.cut()
cut word:                          user.cut_word()
cut line:                          user.cut_line()
cut head:                          user.cut_line_start()
cut tail:                          user.cut_line_end()

copy it:                           edit.copy()
copy word:                         user.copy_word()
copy line:                         user.copy_line()
copy head:                         user.copy_line_start()
copy tail:                         user.copy_line_end()

paste it:                          edit.paste()
(clone | dupe) line:               edit.line_clone()

drag up [<number_small>]:          user.line_swap_up(number_small or 1)
drag down [<number_small>]:        user.line_swap_down(number_small or 1)

# ----- Save -----
save it:                           edit.save()

# ----- Find / Replace -----
find [<user.text>]:                edit.find(text or "")
find all [<user.text>]:            user.find_all(text or "")
find file [<user.text>]:           user.find_file(text or "")
find recent [<user.text>]:         user.find_file_recent(text or "")
find (previous | prev):            edit.find_previous()
find next:                         edit.find_next()
find replace [<user.text>]:        user.find_replace(text or "")
replace word:                      user.find_replace_word()
replace all:                       user.find_replace_all()

# ----- Misc -----
spamma:                            ", "
colgap | coalgap:                  ": "

# ----- Brackets -----
args:
	"()"
	key(left)
index:
	"[]"
	key(left)
diamond:
	"<>"
	key(left)
block:
	"{}"
	key(left)