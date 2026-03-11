then:                       skip()
stop:                       user.stop_app()

pick <number_small>:        user.pick_item(number_small)
pick to:                    user.pick_item(2)
pick <user.word>:
    insert("{word}")
    key(enter)
pick <user.letters>:
    insert("{letters}")
    key(enter)
