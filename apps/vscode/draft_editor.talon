not app: vscode
-

draft (this | dis):
    user.draft_editor_open()
draft all:
    edit.select_all()
    user.draft_editor_open()
draft line:
    edit.select_line()
    user.draft_editor_open()
draft top:
    edit.extend_file_start()
    user.draft_editor_open()
draft bottom:
    edit.extend_file_end()
    user.draft_editor_open()