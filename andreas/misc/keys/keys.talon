# ------- Public keys, No prefix -------

# Public symbol keys: !, %, _
{user.key_symbol}:           "{key_symbol}"

# Public special keys.
enter:                       key(enter)
tab:                         key(tab)
(escape | esc | stop):       user.key_escape()

# ------- Prefixed keys -------

# All un/non modifier keys: [a-z], [0-9], [F1-F12], arrow, symbols
key <user.key_unmodified>:   key(key_unmodified)

# Modifier(s) + key: "control alpha" or "control win left"
key <user.key_modifiers> <user.key_unmodified>:
	key("{key_modifiers}-{key_unmodified}")