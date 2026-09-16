^system shutdown [{user.abort_phrase}]$:
    user.system_shutdown()
^system restart [{user.abort_phrase}]$:
    user.system_restart()
^system hibernate [{user.abort_phrase}]$:
    user.talon_sleep()
    user.system_hibernate()
^system lock [{user.abort_phrase}]$:
    user.talon_sleep()
    user.system_lock()

open settings:
    app.preferences()

open path {user.path}:
    user.file_manager_open(path)

open browser {user.website}:
    user.browser_open(website)

launch {user.launch_command}:
    user.exec(launch_command)
