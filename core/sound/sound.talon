volume up:                  user.volume_up()
volume down:                user.volume_down()
volume mute:                key(mute)

media next:                 key(next)
media last:                 key(prev)
media (play | pause):       key(play_pause)
media stop:                 key(stop)

^playback {user.playback_device}:
    user.notify("Playback: {playback_device}")
    user.change_sound_device(playback_device)

^microphone {user.microhpone_device}:
    user.notify("Microphone: {microhpone_device}")
    user.change_sound_device(microhpone_device)

key(mute):                  user.sound_microphone_toggle()
