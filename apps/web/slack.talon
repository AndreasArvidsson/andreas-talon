app: slack
-

sidebar (show | hide):      key(ctrl-shift-d)
panel (show | hide):        key(ctrl-.)

go unreads:                 key(ctrl-shift-a)
go threads:                 user.slack_open_search_result("Threads")
go [direct] messages:       key(ctrl-shift-k)
go (mentions | reactions):  key(ctrl-shift-m)
go drafts:                  user.slack_open_search_result("Drafts")

scout channel [<user.phrase>]:
    key(ctrl-k)
    insert(phrase or "")
pop channel <user.phrase>:
    user.slack_open_search_result(phrase)

please [<user.phrase>]$:
    key(ctrl-k)
    sleep(100ms)
    edit.delete()
    sleep(100ms)
    insert(phrase or "")

channel last:               key(alt-up)
channel next:               key(alt-down)
channel unread last:        key(alt-shift-up)
channel unread next:        key(alt-shift-down)
next unread:                key(alt-shift-down)

edit last:                  key(ctrl-up)
edit:                       key(e)

format code:                key(ctrl-shift-c)
format [code] block:        key(ctrl-alt-shift-c)
format quote:               key(ctrl-shift-9)
