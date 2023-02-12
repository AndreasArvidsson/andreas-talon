mode: user.game
tag: user.game_commands
app: diablo3
-

# ---------- Sleep mode ----------
{user.sleep_phrase} [<phrase>]$: user.talon_sleep()

# ---------- Abort/Cancel ----------
{user.abort_phrase}$:       skip()

# ---------- Keys ----------

# Letters [A-Z]
{user.letter}:              key(letter)

# Symbol keys: !, %, _
{user.key_symbol}:          key(key_symbol)

# Digits [0-9]
{user.key_number}:          key(key_number)

# Special keys.
(enter | okay):             key(enter)
tab:                        key(tab)
stop:                       key(escape)

# Modifier(s) + key: "control air" or "control win left"
<user.key_modifiers> <user.key_unmodified>:
    key("{key_modifiers}-{key_unmodified}")

# Single key. Including Modifiers, [a-z], [0-9], [F1-F12], arrow, symbols
press <user.key_any>:       key(key_any)
