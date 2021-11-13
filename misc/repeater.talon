twice:                                core.repeat_command(1)
trice:                                core.repeat_command(2)
<number_small> times:                 core.repeat_command(number_small - 1)
<user.ordinals_small>:                core.repeat_command(ordinals_small - 1)
repeat <number_small> times:          core.repeat_command(number_small)

phrase <number_small> times:          core.repeat_partial_phrase(number_small - 1)
repeat phrase <number_small> times:   core.repeat_partial_phrase(number_small)