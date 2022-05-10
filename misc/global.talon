then:   skip()
stop:   user.stop_app()
clip show | clippy:
    user.clipboard_manager_toggle()

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