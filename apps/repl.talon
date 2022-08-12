os: windows
and app.exe: cmd.exe
os: windows
and app.exe: WindowsTerminal.exe
title: Talon - REPL
-

events tail:                "events.tail('/^((?!win|browser).)*$/')\n"
parrot events:              "events.tail('parrot predict')\n"
