^help active$:                         user.help_show_toggle()
^help search <user.words>$:            user.help_search(words)
^help context {user.help_contexts}$:   user.help_context(help_contexts)

^help alphabet$:                       user.help_show_alphabet_toggle()
^help (format|formatters)$:            user.formatters_help_toggle()