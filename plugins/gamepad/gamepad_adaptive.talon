not mode: user.game
not tag: user.gamepad_tester
-

# For xbox adaptive controller only

# DPAD buttons
gamepad(00000000000000000000000000000000:dpad_left:down): user.key_hold("left")
gamepad(00000000000000000000000000000000:dpad_left:up): user.key_release("left")
gamepad(00000000000000000000000000000000:dpad_up:down): user.key_hold("up")
gamepad(00000000000000000000000000000000:dpad_up:up): user.key_release("up")
gamepad(00000000000000000000000000000000:dpad_right:down): user.key_hold("right")
gamepad(00000000000000000000000000000000:dpad_right:up): user.key_release("right")
gamepad(00000000000000000000000000000000:dpad_down:down): user.key_hold("down")
gamepad(00000000000000000000000000000000:dpad_down:up): user.key_release("down")

# Compass / ABXY buttons
# A
gamepad(00000000000000000000000000000000:south:down): key(space)
gamepad(00000000000000000000000000000000:south:up): skip()
# B
gamepad(00000000000000000000000000000000:east:down): key(play_pause)
gamepad(00000000000000000000000000000000:east:up): skip()

# # Select / Start buttons
gamepad(00000000000000000000000000000000:select:down): user.sound_microphone_enable(false)
gamepad(00000000000000000000000000000000:select:up): skip()
gamepad(00000000000000000000000000000000:start:down):
    user.sound_microphone_enable(true)
    user.dictation_mode_exit()
gamepad(00000000000000000000000000000000:start:up): skip()
