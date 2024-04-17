not tag: user.gamepad_tester
-

# For xbox adaptive controller only

# DPAD buttons
gamepad(00000000000000000000000000000000:dpad_left:down): skip()
gamepad(00000000000000000000000000000000:dpad_left:up): skip()
gamepad(00000000000000000000000000000000:dpad_up:down): skip()
gamepad(00000000000000000000000000000000:dpad_up:up): skip()
gamepad(00000000000000000000000000000000:dpad_right:down): skip()
gamepad(00000000000000000000000000000000:dpad_right:up): skip()
gamepad(00000000000000000000000000000000:dpad_down:down): skip()
gamepad(00000000000000000000000000000000:dpad_down:up): skip()

# Compass / ABXY buttons
# A
gamepad(00000000000000000000000000000000:south:down): key(space)
gamepad(00000000000000000000000000000000:south:up): skip()
# B
gamepad(00000000000000000000000000000000:east:down): skip()
gamepad(00000000000000000000000000000000:east:up): skip()

# # Select / Start buttons
gamepad(00000000000000000000000000000000:select:down): user.sound_microphone_enable(false)
gamepad(00000000000000000000000000000000:select:up): skip()
gamepad(00000000000000000000000000000000:start:down): user.sound_microphone_enable(true)
gamepad(00000000000000000000000000000000:start:up): skip()
