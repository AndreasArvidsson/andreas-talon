then:   skip()
stop:   user.stop_app()

pick <number_small>:
    user.pick_item(number_small - 1)
pick to:
    user.pick_item(1)
pick <user.word>:
    "{word}"
    key(enter)
pick <user.letters>:
    "{letters}"
    key(enter)

^cursorless use release$:
    user.cursorless_use_release()
^cursorless use develop$:
    user.cursorless_use_develop()
