mode: command
mode: dictation
-

^talon sleep$:
	speech.disable()
	user.mouse_sleep()
	app.notify("Sleeping")

drowse [<phrase>]$:
	speech.disable()
	user.mouse_sleep()
	app.notify("Sleeping")