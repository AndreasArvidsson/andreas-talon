mode: user.game
app: space_marine
-

settings():
    key_hold = 32

switch:                     key(v)
reload:                     key(r)
focus:                      key(t)
stimms:                     key(f)
frag | grenade:             key(g)
ability:                    key(q)
lock:                       key(x)
sprint:                     key(shift)

use | interact:
    key(e:down)
    sleep(1s)
    key(e:up)

stop:                       key(escape)
okay:                       key(enter)
