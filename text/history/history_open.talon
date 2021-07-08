mode: user.history
-

^history hide$:                  user.history_hide()
^history clear$:                 user.history_clear()
history remove <number_small>:   user.history_remove(number_small)
history repeat <number_small>:   insert(user.history_get_phrase(number_small))
history copy <number_small>:     clip.set_text(user.history_get_phrase(number_small))

history add that:
	text = edit.selected_text()
	user.history_add_phrase(text)