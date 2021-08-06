volume up:              user.volume_up()
volume down:            user.volume_down()
volume mute:            key(mute)

media next:             key(next)
media last:             key(prev)
media (play | pause):   key(play_pause)
media stop:             key(stop)

playback {user.playback_device}:
    app.notify("Playback device:\n{playback_device}")
    user.change_sound_device(playback_device, 0)

microphone {user.microhpone_device}:
    app.notify("Microphone device:\n{microhpone_device}")
    user.change_sound_device(microhpone_device, 2)