not tag: user.cursorless
-

# ----- Cut, copy, paste -----
cut (this | dis):           edit.cut()
copy (this | dis):          edit.copy()
paste to (this | dis):      edit.paste()

# ----- Word -----
take token:                 edit.select_word()
cut token:                  user.cut_word()
copy token:                 user.copy_word()
paste to token:             user.paste_word()
(chuck | clear) token:      edit.delete_word()

# Line
pre line:                   edit.line_start()
post line:                  edit.line_end()
take line:                  edit.select_line()
cut line:                   user.cut_line()
copy line:                  user.copy_line()
paste to line:              user.paste_line()
chuck line:                 edit.delete_line()
clear line:                 user.clear_line()
clone line:                 edit.line_clone()
drink line:                 edit.line_insert_up()
pour line:                  edit.line_insert_down()

# Head / tail
take head:                  user.select_line_start()
take tail:                  user.select_line_end()
cut head:                   user.cut_line_start()
cut tail:                   user.cut_line_end()
copy head:                  user.copy_line_start()
copy tail:                  user.copy_line_end()
paste to head:              user.paste_line_start()
paste to tail:              user.paste_line_end()
(chuck | clear) head:       user.delete_line_start()
(chuck | clear) tail:       user.delete_line_end()

# Paragraph
pre block:                  edit.paragraph_start()
post block:                 edit.paragraph_end()
take block:                 edit.select_paragraph()
cut block:                  user.cut_paragraph()
copy block:                 user.copy_paragraph()
paste to block:             user.paste_paragraph()
(chuck | clear) block:      edit.delete_paragraph()

# File / document
pre file:                   edit.file_start()
post file:                  edit.file_end()
take file:                  edit.select_all()
cut file:                   user.cut_all()
copy file:                  user.copy_all()
paste to file:              user.paste_all()
(chuck | clear) file:       user.delete_all()

# Selection
clone this:                 edit.selection_clone()

# Reformat
<user.formatters> (format|form) this:
    user.reformat_selection(formatters)
<user.formatters> (format|form) token:
    edit.select_word()
    user.reformat_selection(formatters)
<user.formatters> (format|form) line:
    edit.select_line()
    user.reformat_selection(formatters)

# Homophones
phones this:                user.homophones_cycle_selected()
phones token:
    edit.select_word()
    user.homophones_cycle_selected()

# Wrappers
{user.delimiter_pair_wrap} wrap this:
    user.delimiters_pair_wrap_selection(delimiter_pair_wrap)
{user.delimiter_pair_wrap} wrap token:
    edit.select_word()
    user.delimiters_pair_wrap_selection(delimiter_pair_wrap)
{user.delimiter_pair_wrap} wrap line:
    edit.select_line()
    user.delimiters_pair_wrap_selection(delimiter_pair_wrap)
