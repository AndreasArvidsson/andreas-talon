<user.repeater_phrase>:                 core.repeat_command(repeater_phrase)
repeat <user.repeater_phrase>:          core.repeat_command(repeater_phrase + 1)

phrase <user.repeater_phrase>:          core.repeat_partial_phrase(repeater_phrase)
repeat phrase <user.repeater_phrase>:   core.repeat_partial_phrase(repeater_phrase + 1)