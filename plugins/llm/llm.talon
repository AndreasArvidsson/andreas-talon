model fix <user.prose>:
    user.model_process_selected_text("custom", prose)

model emoji <user.prose>:
    user.model_insert_processed_text("emoji", prose)

model insert <user.prose>:
    user.model_insert_processed_text(prose)

model test:
    user.model_insert_processed_prompt("write a short story about pirates")
    # user.model_insert_processed_prompt("Write a short story about pirates. 300 words or less.")
