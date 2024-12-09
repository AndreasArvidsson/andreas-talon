^help active$:              user.help_active_toggle()
^help search <user.prose>$: user.help_search(prose)
^help context {user.help_contexts}$: user.help_context(help_contexts)

^help <user.prose> commands$: user.help_search_commands(prose)
^help <user.prose> actions$: user.help_search_actions(prose)

^help alphabet$:            user.help_alphabet_toggle()
^help scope$:               user.help_scope_toggle()
^help (format | formatters)$: user.help_formatters_toggle()
^help (running | focus)$:   user.help_running_apps_toggle()

^help key$:                 user.help_key_debug_toggle()
