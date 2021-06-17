mode: user.demo
-

^demo mode off$:
	mode.disable("user.demo")
	app.notify("Demo mode off")

<phrase>:   skip()