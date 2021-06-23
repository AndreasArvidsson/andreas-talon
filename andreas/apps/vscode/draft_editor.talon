draft this:
	user.draft_editor_open()

draft all:
    edit.select_all()
	user.draft_editor_open()

draft line:
    edit.select_line()
	user.draft_editor_open()

draft save:
    user.draft_editor_save()