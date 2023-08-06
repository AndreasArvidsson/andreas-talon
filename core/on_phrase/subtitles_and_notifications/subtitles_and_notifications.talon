settings():
    # ==============================
    # SUBTITLE SETTINGS
    # ==============================

    # Show subtitles
    user.subtitles_show = true
    # Show subtitles on all screens
    user.subtitles_all_screens = true
    # 100px subtitles font size
    user.subtitles_size = 100
    # White subtitles color
    user.subtitles_color = "ffffff"
    # Slightly dark subtitle outline
    user.subtitles_color_outline = "aaaaaa"
    # For each character in the subtitle extend the timeout 50ms
    user.subtitles_timeout_per_char = 50
    # 750ms is the minimum timeout for a subtitle
    user.subtitles_timeout_min = 750
    # 3 seconds is the maximum timeout for a subtitle
    user.subtitles_timeout_max = 3000
    # Subtitles are positioned at the bottom of the screen
    user.subtitles_y = 0.93

    # ==============================
    # NOTIFICATION SETTINGS
    # ==============================

    # Show notifications
    user.notifications_show = true
    # Show notifications on all screens
    user.notifications_all_screens = true
    # 100px notifications font size
    user.notifications_size = 100
    # Blue notifications color
    user.notifications_color = "6495ED"
    # Slightly dark notification outline
    user.notifications_color_outline = "41609a"
    # For each character in the notification extend the timeout 50ms
    user.notifications_timeout_per_char = 50
    # 1.5 seconds is the minimum timeout for a notification
    user.notifications_timeout_min = 1500
    # 5 seconds is the maximum timeout for a notification
    user.notifications_timeout_max = 5000
    # Notifications are centered vertically
    user.notifications_y = 0.5

subtitles (show | hide):    user.toggle_subtitles()
