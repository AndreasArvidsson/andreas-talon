# tag(): user.key_debug

settings():
    # Speech timeout
    speech.timeout = 0.25
    # Record speech
    speech.record_all = true
    # Disable Talon subtitles
    speech._subtitles = false

    # Print timings for spoken phrases
    user.print_phrase_timings = false

    # Pretty print spoken phrases
    user.pretty_print_phrase = true

    # Show mode indicator
    user.mode_indicator_show = true

    # Location to store cursorless settings
    user.cursorless_settings_directory = "andreas-talon/settings/cursorless-settings"

    # Mouse scroll speed
    user.scroll_speed = 0.7

    # General gui
    # imgui.scale = 1.25
    user.gui_max_rows = 5
    user.gui_max_cols = 80

    # Help gui
    user.help_max_command_lines_per_page = 50
    user.help_max_contexts_per_page = 50
    user.help_scope_max_length = 80

    # Command history
    user.command_history_size = 20

    # Cursorless
    user.cursorless_spoken_form_test_restore_microphone = "System Default"
    # user.private_cursorless_use_preferred_scope = false
