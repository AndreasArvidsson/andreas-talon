open settings:      app.preferences()

system shutdown:    user.system_shutdown()
system restart:     user.system_restart()
system hibernate:   user.system_hibernate()
system lock:        key(super-l)

show desktop:       key(super-d)

app open {user.launch_command}:
    user.exec(launch_command)

path open {user.path}:
    user.exec(path)

browser open {user.webpage}:
    user.focus_name("Firefox")
    user.browser_open(webpage)