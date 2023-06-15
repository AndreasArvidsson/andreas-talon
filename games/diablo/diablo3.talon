mode: user.game
tag: user.game_voip_muted
app: diablo3
app: diablo4
-

# ---------- Abort/Cancel ----------
{user.abort_phrase}$:       user.abort_phrase_command()

# ---------- Discord ----------
discord:                    key(ctrl-shift-´)

# ---------- Toggle fps meter ----------
show fps:                   key(ctrl-r)

# ---------- Keys ----------

{user.letter}:              key(letter)
(enter | okay):             key(enter)
tab:                        key(tab)
stop:                       key(escape)
void:                       key(space)

# Modifier(s) + key: "control air" or "control win left"
<user.key_modifiers> <user.key_unmodified>:
    key("{key_modifiers}-{key_unmodified}")

# Single key. Including Modifiers, [a-z], [0-9], [F1-F12], arrow, symbols
press <user.key_any>:       key(key_any)

# Skip cutscenes
skip:
    key(escape:down)
    sleep(1s)
    key(escape:up)
    sleep(50ms)
    key(escape)
