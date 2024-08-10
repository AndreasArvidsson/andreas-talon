model fix this:
    user.model_process_selected_text("fix")

model fix <user.prose>:
    user.model_process_selected_text("custom", prose)

model emoji <user.prose>:
    user.model_insert_processed_text("emoji", prose)

model insert <user.prose>:
    user.model_insert_processed_prompt(prose)

model fix <user.cursorless_target>:
    text = user.cursorless_get_text(cursorless_target)
    fixed_text = user.model_process_text("fix", text)
    destination = user.cursorless_create_destination(cursorless_target)
    user.cursorless_insert(destination, fixed_text)
