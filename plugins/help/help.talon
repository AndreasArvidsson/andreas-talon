^help active$:              user.help_active_toggle()
^help search <user.phrase>$: user.help_search(phrase)
^help context {user.help_contexts}$: user.help_context(help_contexts)

^help <user.phrase> commands$: user.help_search_commands(phrase)
^help <user.phrase> actions$: user.help_search_actions(phrase)

^help alphabet$:            user.help_alphabet_toggle()
^help scope$:               user.help_scope_toggle()
^help (format | formatters)$: user.help_formatters_toggle()
^help (running | focus)$:   user.help_running_apps_toggle()

^help key$:                 user.help_key_debug_toggle()
