os: windows
-

task view:                  key(super-tab)
task manager:               key(ctrl-shift-escape)
windows:                    key("ctrl-alt-tab")
show desktop:               key(super-d)

start menu:                 key(super)
context menu:               key(super-x)

open notepad:               user.exec("notepad")
open paint:                 user.exec("mspaint")
open sound settings:        user.exec("control mmsys.cpl sounds")
open control panel:         user.exec("control")
open system settings:       key(super-i)
open explorer:              key(super-e)

(start | stop) recording:   key(alt-f9)

scout app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
pop app [<user.text>]$:
    key(super-s)
    "apps: {text or ''}"
    key(enter)