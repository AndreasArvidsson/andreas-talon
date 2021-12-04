# Letters [A-Z]
{user.key_alphabet}:         key(key_alphabet)

# Symbol keys: !, %, _
{user.key_symbol}:           key(key_symbol)

# Digits [0-9]
{user.key_number}:           key(key_number)

# Special keys.
(enter | okay):              key(enter)
tab:                         key(tab)
escape:                      key(escape)
caps lock:                   key(capslock)
num lock:                    key(numlock)

# Special symbols
new line symbol:             "\\n"
tab symbol:                  "\\t"

# Modifier(s) + key: "control alpha" or "control win left"
<user.key_modifiers> <user.key_unmodified>:
    key("{key_modifiers}-{key_unmodified}")

# All un/non modifier keys: [a-z], [0-9], [F1-F12], arrow, symbols
key <user.key_unmodified>:   key(key_unmodified)

# Add symbol at end of line and then insert line below
push {user.key_symbol}:
    edit.line_end()
    "{key_symbol}"
    edit.line_insert_down()