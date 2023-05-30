then:                       skip()
stop:                       user.stop_app()

pick <number_small>:        user.pick_item(number_small)
pick to:                    user.pick_item(2)
pick <user.word>:
    "{word}"
    key(enter)
pick <user.letters>:
    "{letters}"
    key(enter)
