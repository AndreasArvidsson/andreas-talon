then:        skip()
stop:        user.stop_app()
clip show:   user.clipboard_manager_toggle()

pick <number_small>:
    user.pick_item(number_small - 1)
pick <user.words>:
    "{words}"
    key(enter)
pick <user.letters>:
    "{letters}"
    key(enter)