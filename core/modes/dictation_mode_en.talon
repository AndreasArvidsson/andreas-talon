mode: dictation
-

settings():
    speech.engine = "wav2letter-wisp"

# Freely dictate text
<user.prose>:               "{prose}"

# Insert the actual words
# Only words, no symbols or numbers
escape <user.phrase>$:      "{phrase}"
escape <user.phrase> over:  "{phrase}"

^bullet:                    "* "
^task:                      "- [ ] "

^indent:                    edit.indent_more()
^dedent:                    edit.indent_less()

new line:
    edit.line_insert_down()
    user.dictation_format_reset()

new (graph | block):
    edit.line_insert_down()
    edit.line_insert_down()
    user.dictation_format_reset()

# Switch to command mode and insert a phrase
(command mode | over) [<phrase>]$:
    user.command_mode(phrase or "")

# Switch to sleep mode
{user.sleep_phrase} [<phrase>]$: user.talon_sleep()
