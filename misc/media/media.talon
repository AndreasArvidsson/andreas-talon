volume up:              user.volume_up()
volume down:            user.volume_down()
volume mute:            key(mute)

media next:             key(next)
media last:             key(prev)
media (play | pause):   key(play_pause)
media stop:             key(stop)

playback {user.playback_devices}:
	user.change_playback_device(playback_devices)