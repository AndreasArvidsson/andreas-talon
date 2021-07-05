^(format | formatters) (show | help)$:
	user.formatters_help_toggle()

<user.format_text>$:        user.insert_string(format_text)
<user.format_text> over:    user.insert_string(format_text)

<user.formatters> this:     user.formatters_reformat_selection(formatters)
<user.formatters> last:     user.formatters_reformat_last(formatters)

<user.formatters> word:
	edit.select_word()
	user.formatters_reformat_selection(formatters)