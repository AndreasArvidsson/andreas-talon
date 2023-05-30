# Subtitles and notifications

Custom subtitles and notifications with settings to tweak color, position and timeout.

Talons default subtitles needs to be disabled to avoid duplicates.

![Subtitle](./images/subtitle.png)

![Notification](./images/notification.png)

## Use subtitles

```python
from talon import speech_system, actions

def on_pre_phrase(phrase):
    words = phrase.get("phrase")

    if words and actions.speech.enabled():
        text = " ".join(words)
        show_subtitle(text)

speech_system.register("pre:phrase", on_pre_phrase)
```

## Show / hide subtitles

Subtitles can either be controlled via a setting
or a voice command.

### Show subtitles

Setting: `user.subtitles_show = true`  
Say: `"subtitles show"`

### Hide subtitles

Setting: `user.subtitles_show = false`  
Say: `"subtitles hide"`

## Use notifications

```python
actions.user.notify("Some notification")
```

## Show / hide notifications

Notifications are controlled via settings.

### Show notifications

Setting: `user.notifications_show = true`

### Hide notifications

Setting: `user.notifications_show = false`
