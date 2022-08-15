# Since the foot switch uses keypad numbers make sure that `num lock` is turned off.

# Top button
key(keypad_0:down):         user.foot_switch_down(0)
key(keypad_0:up):           user.foot_switch_up(0)

# Center button
key(keypad_1:down):         user.foot_switch_down(1)
key(keypad_1:up):           user.foot_switch_up(1)

# # button
key(keypad_2:down):         user.foot_switch_down(2)
key(keypad_2:up):           user.foot_switch_up(2)

# Right button
key(keypad_3:down):         user.foot_switch_down(3)
key(keypad_3:up):           user.foot_switch_up(3)


# Misc

scroll reverse:             user.foot_switch_scroll_reverse()
