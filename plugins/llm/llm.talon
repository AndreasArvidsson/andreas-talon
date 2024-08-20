model fix <user.prose>:
    user.model_process_selected_text("custom", prose)

model emoji <user.prose>:
    user.model_insert_processed_text("emoji", prose)

model insert <user.prose>:
    user.model_insert_processed_prompt_streaming(prose)

model test:
    # user.model_insert_processed_prompt_streaming("Hello there")
    user.model_insert_processed_prompt_streaming("write a short story about pirates")
    # user.model_insert_processed_prompt_streaming("Write a short story about pirates. 300 words or less.")
    # user.model_insert_processed_prompt("Write a short story about pirates. 300 words or less.")

# Im giving this two you. do you want it. If so, why???
