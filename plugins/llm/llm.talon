model fix this:
    user.model_process_selected_text("fix")

model fix this as <user.text>:
    user.model_process_selected_text("custom", text)

model custom <user.text>:
    user.model_insert_processed_prompt(text)

model fix <user.cursorless_target>:
    text = user.cursorless_get_text(cursorless_target)
    fixed_text = user.model_process_text("fix", text)
    destination = user.cursorless_create_destination(cursorless_target)
    user.cursorless_insert(destination, fixed_text)
