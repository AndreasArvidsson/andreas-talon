not tag: user.gamepad_tester
-

# For xbox adaptive controller only

# # Select / Start buttons
gamepad(00000000000000000000000000000000:select:down): user.sound_microphone_enable(false)
gamepad(00000000000000000000000000000000:select:up): skip()

gamepad(00000000000000000000000000000000:start:down): user.sound_microphone_enable(true)
gamepad(00000000000000000000000000000000:start:up): skip()
