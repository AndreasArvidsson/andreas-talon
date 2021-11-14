go settings:        app.preferences()

system shutdown:    user.system_shutdown()
system restart:     user.system_restart()
system hibernate:   user.system_hibernate()
system lock:        key(super-l)

show desktop:       key(super-d)

open {user.launch_command}:
    user.exec(launch_command)