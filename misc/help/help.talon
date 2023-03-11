^help active$:              user.help_active_toggle()
^help search <user.text>$:  user.help_search(text)
^help context {user.help_contexts}$: user.help_context(help_contexts)

^help <user.text> commands$: user.help_search_commands(text)
^help <user.text> actions$: user.help_search_actions(text)

^help alphabet$:            user.help_alphabet_toggle()
^help scope$:               user.help_scope_toggle()
^help (format|formatters)$: user.help_formatters_toggle()
^help (running|focus)$:     user.help_running_apps_toggle()

^help key$:                 user.help_key_debug_toggle()
