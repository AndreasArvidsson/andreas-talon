# Letters [A-Z]
{user.letter}:              key(letter)

# Symbol keys: !, %, _
{user.symbol}:              key(symbol)

# Digits [0-9]
{user.digit}:               key(digit)

# Special keys.
enter | okay:               key(enter)
tab:                        key(tab)

# Special symbols
new line [symbol]:          "\\n"
tab symbol:                 "\\t"

# Add symbol at end of line and then insert line below
spike {user.symbol}:        user.insert_symbol_and_break_at_end(symbol)

# Add symbol padded/surrounded by whitespace
pad {user.symbol}:          " {symbol} "

# Modifier(s) + key: "control air" or "control win left"
<user.key_modifiers> <user.key_unmodified>:
    key("{key_modifiers}-{key_unmodified}")

# Single key. Including Modifiers, [a-z], [0-9], [F1-F12], arrow, symbols
press <user.key_any>:       key(key_any)
