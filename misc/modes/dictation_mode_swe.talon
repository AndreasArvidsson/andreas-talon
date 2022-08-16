mode: dictation
language: sv_SE
-

# Freely dictate text
<user.prose>:               "{prose}"

^listpunkt:                 "* "
^uppgift:                   "- [ ] "

^indrag:                    edit.indent_more()
^utdrag:                    edit.indent_less()

ny rad:
    edit.line_insert_down()
    user.dictation_format_reset()

ny (paragraf | graf):
    edit.line_insert_down()
    edit.line_insert_down()
    user.dictation_format_reset()

# Switch to command mode
(command mode | over | över)$:
    user.command_mode()
