os: windows
and app.name: Windows Command Processor
os: windows
and app.exe: cmd.exe
title: Talon - REPL
-

events tail:                "events.tail('/^((?!win|browser).)*$/')\n"
parrot events:              "events.tail('parrot predict')\n"
