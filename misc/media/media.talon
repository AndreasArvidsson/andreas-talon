volume up:              user.volume_up()
volume down:            user.volume_down()
volume mute:            key(mute)

media next:             key(next)
media last:             key(prev)
media (play | pause):   key(play_pause)
media stop:             key(stop)

playback {user.playback_device}:
    user.notify("Playback device: {playback_device}")
    user.change_sound_device(playback_device, 1)
    user.change_sound_device(playback_device, 2)

microphone {user.microhpone_device}:
    user.notify("Microphone device: {microhpone_device}")
    user.change_sound_device(microhpone_device, 1)
    user.change_sound_device(microhpone_device, 2)