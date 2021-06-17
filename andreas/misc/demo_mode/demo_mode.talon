mode: user.demo
-

^demo mode$:
	mode.disable("user.demo")
	app.notify("Demo mode off")

<phrase>:   skip()