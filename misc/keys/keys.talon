# Letters [A-Z]
{user.letter}:          key(letter)

# Symbol keys: !, %, _
{user.key_symbol}:      key(key_symbol)

# Digits [0-9]
{user.key_number}:      key(key_number)

# Special keys.
(enter | okay):         key(enter)
tab:                    key(tab)
void:                   key(" ")

# Special symbols
new line [symbol]:      "\\n"
tab symbol:             "\\t"

# Modifier(s) + key: "control alpha" or "control win left"
<user.key_modifiers> <user.key_unmodified>:
    key("{key_modifiers}-{key_unmodified}")

# Single key. Including Modifiers, [a-z], [0-9], [F1-F12], arrow, symbols
press <user.key_any>:   key(key_any)

# Add symbol at end of line and then insert line below
push {user.key_symbol}:
    edit.line_end()
    "{key_symbol}"
    edit.line_insert_down()