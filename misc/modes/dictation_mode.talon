mode: dictation
-

# Freely dictate text
<user.prose>:                        auto_insert(prose)

# Switch to command mode and insert a phrase
(command mode | over) [<phrase>]$:   user.command_mode(phrase or "")

# Insert the actual words
escape over:                         auto_insert("over")
escape command mode:                 auto_insert("command mode")