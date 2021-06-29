^(format | formatters) (show | help)$:
	user.formatters_help_toggle()

<user.formatters> this:   user.formatters_reformat_selection(formatters)
<user.formatters> last:   user.formatters_reformat_last(formatters)

<user.formatters> word:
	edit.select_word()
	user.formatters_reformat_selection(formatters)