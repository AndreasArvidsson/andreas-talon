mode: dictation
language: sv
-

# Freely dictate text
<user.prose>:               "{prose}"

^(listpunkt | list punkt):  "* "
^uppgift:                   "- [ ] "

^(indrag | in drag):        edit.indent_more()
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

# Switch to sleep mode
{user.sleep_phrase} [<phrase>]$: user.talon_sleep()
