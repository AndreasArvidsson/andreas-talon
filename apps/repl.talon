os: windows
and app.exe: cmd.exe
os: windows
and app.exe: conhost.exe
os: windows
and app.exe: windowsterminal.exe
title: Talon - REPL
-

terminate:                  key(ctrl-c)

events tail:                "events.tail('/^((?!win|browser).)*$/')\n"
parrot events:              "events.tail('parrot predict')\n"

actions list [<user.prose>]:
    insert('actions.list("{prose or ""}")')
    key(left:2)
