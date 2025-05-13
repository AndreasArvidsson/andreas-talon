mode: dictation
language: sv
-

settings():
    speech.engine = "webspeech"

# Freely dictate text
<user.prose>:               "{prose}"

^(listpunkt | list punkt):  "* "
^uppgift:                   "- [ ] "

^(indrag | in drag):        edit.indent_more()
^utdrag:                    edit.indent_less()

(ny | nu) rad:
    edit.line_insert_down()
    user.dictation_format_reset()

(ny | nu) (paragraf | graf):
    edit.line_insert_down()
    edit.line_insert_down()
    user.dictation_format_reset()

# Switch to command mode
(command mode | over | över)$:
    user.command_mode()

# Switch to sleep mode
{user.sleep_phrase} [<phrase>]$: user.talon_sleep()
