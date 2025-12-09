app: talon_repl
-

terminate:                  key(ctrl-c)

events tail:                "events.tail()\n"
parrot events:              "events.tail('parrot predict')\n"

actions list [<user.prose>]:
    insert('actions.list("{prose or ""}")')
    key(left:2)
