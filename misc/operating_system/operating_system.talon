open settings:      app.preferences()

system shutdown:    user.system_shutdown()
system restart:     user.system_restart()
system hibernate:   user.system_hibernate()
system lock:        key(super-l)

open {user.launch_command}:
    user.exec(launch_command)

open path {user.path}:
    user.exec(path)

open browser {user.webpage}:
    user.browser_focus_open(webpage)