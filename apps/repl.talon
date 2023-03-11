os: windows
and app.exe: cmd.exe
os: windows
and app.exe: WindowsTerminal.exe
title: Talon - REPL
-

events tail:                "events.tail('/^((?!win|browser).)*$/')\n"
parrot events:              "events.tail('parrot predict')\n"

actions list [<user.text>]:
    'actions.list("{text or ""}")'
    key(left:2)
